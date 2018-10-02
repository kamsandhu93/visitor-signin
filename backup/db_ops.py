import sys
import hashlib
import configparser
import argparse
import logging
import time
import os
import dropbox

from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

def main():
    arguments = parseArgs(sys.argv[1:])
    config = parseConfig(arguments.config)
    startLogging(config, arguments.operation)
    database = Database(config)
    runOperation(database, arguments.operation, arguments.service)

def parseArgs(args):
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

def checkFile(value):
    if not os.path.isabs(value):
        raise argparse.ArgumentTypeError("{0} is not an absolute path".format(value))

    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("{0} does not exist".format(value))

    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError("{0} is not a file".format(value))

    return value

def checkOperation(value):
    validOperations = ["backup", "restore", "restore_force"]
    if value not in validOperations:
        raise argparse.ArgumentTypeError("{0} is not in a valid operation".format(value))

    return value

def parseConfig(configPath):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(configPath)

    return config.defaults()

def startLogging(config, operation):
    logPath = os.path.join(config["LogDir"], "backup.log")
    loggingFormat = logging.Formatter("%(asctime)s | {0} | %(levelname)s | %(message)s".format(operation))

    fileHandler = logging.FileHandler(logFilePath, encoding = "utf-8")
    fileHandler.setFormatter(loggingFormat)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(loggingFormat)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(fileHandler)
    logging.root.addHandler(consoleHandler)

class Database(object):
    def __init__(self, config):
        self.dbx = dropbox.Dropbox(config["DropboxToken"])
        self.localPath = os.path.join(config["DatabaseDir"], config["DatabaseFile"])
        self.backupPath = os.path.join("/", config["DatabaseFile"])
        self.operationDict = {
            "backup": self.backup,
            "restore": self.restore,
            "restore_force": self.forceRestore
        }

    def backup(self):
        with open(self.localPath, "rb") as f:
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

    def restore(self):
        try:
            if not os.path.exists(self.localPath):
                self.dbx.files_download_to_file(self.localPath, self.backupPath)
                logging.info("Normal restore {0} from dropbox {1}".format(self.localPath, self.backupPath))
        except ApiError as err:
            logging.error(err)
            sys.exit()
        except IOError as err:
            logging.error(err)
            sys.exit()

    def forceRestore(self):
        try:
            self.dbx.files_download_to_file(self.localPath, self.backupPath)
            loggin.info("Forced restore {0} from dropbox {1}".format(self.localPath, self.backupPath))
        except ApiError as err:
            logging.error(err)
            sys.exit()
        except IOError as err:
            logging.error(err)
            sys.exit()

    def operate(self, operation):
        self.operationDict[operation]()

def runOperation(database, operation, isService):
    if isService:
        runAsService(database, operation)
    else:
        database.operate(operation)

def runAsService(database, operation):
    currentHash = {}
    while True:
        newHash = getHash(localPath)
        if newHash != currentHash:
            database.operate(operation)
            currentHash = newHash
        time.sleep(30)

def getHash(filePath, bufferSize=65536):
    sha1 = hashlib.sha1()
    md5 = hashlib.md5()

    with open(filePath, "rb") as f:
        while True:
            data = f.read(bufferSize)
            if not data:
                break
            md5.update(data)
            sha1.update(data)

    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest()
    }

if __name__ == "__main__":
    main()
