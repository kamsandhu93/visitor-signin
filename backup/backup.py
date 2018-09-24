#!/usr/bin/env python2
import dropbox
import sys
import argparse
import logging
import os

from dropbox.exceptions import ApiError, AuthError
from dropbox.files import WriteMode

def startLogging(logFilePath):
    """
    Logging configurations
    """

    loggingFormat = logging.Formatter("%(asctime)s | Backup | %(levelname)s | %(message)s")

    fileHandler = logging.FileHandler(logFilePath, encoding = "utf-8")
    fileHandler.setFormatter(loggingFormat)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(loggingFormat)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(fileHandler)
    logging.root.addHandler(consoleHandler)

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

def argParser(args):
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
        type=checkFile, required=True,
        help="Database file path"
    )

    parser.add_argument(
        "-l", "--log",
        type=checkDirectory, required=True,
        help="Log file path"
    )

    arguments = parser.parse_args(args)
    return arguments


def main():
    """
    Main
    """
    arguments = argParser(sys.argv[1:])

    dbPath = arguments.path
    backupName = "/{0}".format(os.path.split(arguments.path)[1])

    startLogging(os.path.join(arguments.log, "backup.log"))

    dbx = dropbox.Dropbox(arguments.token)

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

if __name__ == "__main__":
    main()
