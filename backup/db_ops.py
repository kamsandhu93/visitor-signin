import sys
import hashlib
import ConfigParser
import argparse
import logging
import dropbox
import time
import os
from functools import partial

from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

class HashHelper(object):
    """
    class for file hashing
    """
    def __init__(self, filePath, bufferSize=65536):
        """
        constuctor
        """
        self.filePath = filePath
        self.bufferSize = bufferSize

    def getHash(self):
        """
        get sha1 value
        """
        sha1 = hashlib.sha1()
        md5 = hashlib.md5()

        with open(self.filePath, "rb") as f:
            while True:
                data = f.read(self.bufferSize)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)

        return {
            "md5": md5.hexdigest(),
            "sha1": sha1.hexdigest()
        }

class DbManager(object):
    """
    class for database backup and restore management
    """
    def __init__(self, apiToken, localPath, backupPath):
        """
        constructor
        """
        self.dbx = dropbox.Dropbox(apiToken)
        self.localPath = localPath
        self.backupPath = backupPath

    def backup(self):
        """
        backup database
        """
        with open (self.localPath, "rb") as f:
            try:
                self.dbx.files_upload(f.read(), self.backupPath, mode=WriteMode("overwrite"))
                logging.info("Backed up {0} to dropbox {1}".format(self.localPath, self.backupPath))
            except ApiError as err:
                if (err.error.is_path() and
                        err.error.get_path().reason.is_insufficient_space()):
                    logging.error("Cannot back up; insufficient space.")
                    sys.exit()
                elif err.user_message_text:
                    logging.error(err.user_message_text)
                    sys.exit()
                else:
                    logging.error(err)
                    sys.exit()

    def restore(self, force=False):
        """
        restore database
        """
        try:
            if force or not os.path.exists(self.localPath):
                self.dbx.files_download_to_file(self.localPath, self.backupPath)

                msg = "Normal restore {0} from dropbox {1}".format(self.localPath, self.backupPath)
                if force:
                    msg = "Forced restore {0} from dropbox {1}".format(self.localPath, self.backupPath)

                logging.info(msg)
        except ApiError as err:
            logging.error(err)
            sys.exit()
        except IOError as err:
            logging.error(err)
            sys.exit()

def checkFile(value):
    """
    Check file path exists, is file and is absolute
    """
    if not os.path.isabs(value):
        raise argparse.ArgumentTypeError("{0} is not an absolute path".format(value))

    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("{0} does not exist".format(value))

    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError("{0} is not a file".format(value))

    return value

def checkOperation(value):
    """
    Check input operation is valid
    """
    validOperations = ["backup", "restore", "restore_force"]
    if value not in validOperations:
        raise argparse.ArgumentTypeError("{0} is not in a valid operation".format(value))

    return value

def parseArgs(args):
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config",
        type=checkFile, required=False,
        default="/visitor-back/db_ops.cfg",
        help="Config file path"
    )

    parser.add_argument(
        "-o", "--operation",
        type=checkOperation, required=True,
        help="Backup or restore database"
    )

    parser.add_argument(
        "-s", "--service",
        dest="service", action="store_true",
        help="Run script continuously as a service"
    )

    parser.set_defaults(service=False)

    arguments = parser.parse_args(args)
    return arguments

def parseConfig(configPath):
    """
    Parse config and return as dictionary
    """
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(configPath)

    return config.defaults()

def startLogging(logFilePath, operation):
    """
    Logging configurations
    """

    loggingFormat = logging.Formatter("%(asctime)s | {0} | %(levelname)s | %(message)s".format(operation))

    fileHandler = logging.FileHandler(logFilePath, encoding = "utf-8")
    fileHandler.setFormatter(loggingFormat)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(loggingFormat)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(fileHandler)
    logging.root.addHandler(consoleHandler)

def main():
    """
    main
    """
    arguments = parseArgs(sys.argv[1:])
    config = parseConfig(arguments.config)

    localPath = os.path.join(config["DatabaseDir"], config["DatabaseFile"])
    backupPath = os.path.join("/", config["DatabaseFile"])
    logPath = os.path.join(config["LogDir"], "backup.log")

    startLogging(logPath, arguments.operation)
    hashHelper = HashHelper(localPath)
    dbManager = DbManager(config["DropboxToken"], localPath, backupPath)

    operationDict = {
        "backup": dbManager.backup,
        "restore": dbManager.restore,
        "restore_force": partial(dbManager.restore, True)
    }

    if arguments.service:
        currentHash = {}
        while True:
            newHash = hashHelper.getHash()
            if newHash != currentHash:
                operationDict[arguments.operation]()
                currentHash = newHash
            time.sleep(30)
    else:
        operationDict[arguments.operation]()
if __name__ == "__main__":
    main()
