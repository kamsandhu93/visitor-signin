#!/usr/bin/env python2
import dropbox
import sys
import argparse
import logging
import os

from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

def checkFile(value):
    """
    Check file exists and is not directory
    """
    if not os.path.isabs(value):
        raise argparse.ArgumentTypeError("{0} is not an absolute path".format(value))

    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("{0} does not exist".format(value))

    if not os.path.isfile(value):
        raise argparse.ArgumentTypeError("{0} is not a file path".format(value))

    return value

def checkDirectory(value):
    """
    Check path is directory and exists
    """
    if not os.path.isabs(value):
        raise argparse.ArgumentTypeError("{0} is not an absolute path".format(value))

    if not os.path.exists(value):
        raise argparse.ArgumentTypeError("{0} does not exist".format(value))

    if os.path.isfile(value):
        raise argparse.ArgumentTypeError("{0} is not a directory".format(value))

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
        "-t", "--token",
        type=str, required=True,
        help="Dropbox api token"
    )

    parser.add_argument(
        "-p", "--path",
        type=checkDirectory, required=True,
        help="Database directory path"
    )

    parser.add_argument(
        "-l", "--log",
        type=checkDirectory, required=True,
        help="Log directory path"
    )

    parser.add_argument(
        "-f", "--file",
        type=str, required=True,
        help="Database file name"
    )

    parser.add_argument(
        "-o", "--operation",
        type=checkOperation, required=True,
        help="Backup or restore database"
    )

    arguments = parser.parse_args(args)
    return arguments

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


def backup(dbx, dbPath, backupName):
    """
    backup database
    """
    with open (dbPath, "rb") as dbFile:
        try:
            dbx.files_upload(dbFile.read(), backupName, mode=WriteMode("overwrite"))
            logging.info("Backed up {0} to dropbox {1}".format(dbPath, backupName))
        except ApiError as err:
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                logging.error("Cannot back up; insufficient space.")
                sys.exit()
            elif err.user_message_text:
                logging.error(err.user_message_text)
                sys.exit()
            else:
                logging.err(err)
                sys.exit()

def restore(dbx, dbPath, backupName, force=None):
    """
    restore database
    """
    if force:
        dbx.files_download_to_file(dbPath, backupName)
    elif not os.path.exists(dbPath):
        dbx.files_download_to_file(dbPath, backupName)


def main():
    """
    Main
    """
    arguments = parseArgs(sys.argv[1:])

    dbPath = os.path.join(arguments.path, arguments.file)
    backupName = "/{0}".format(arguments.file)

    dbx = dropbox.Dropbox(arguments.token)

    startLogging(os.path.join(arguments.log, "backup.log"))

    if arguments.operation == "backup":
        backup(dbx, dbPath, backupName)
    elif arguments.operation == "restore":
        restore(dbx, dbPath, backupName)
    elif arguments.operation == "restore_force":
        restore(dbx, dbPath, backupName, True)


if __name__ == "__main__":
    main()
