#import dropbox
import sys
import argparse
import logging

#from dropbox.exceptions import ApiError, AuthError
#from dropbox.files import WriteMode

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

    arguments = parser.parse_args(args)
    return arguments.token


def main():
    """
    Main
    """

    token = argParser(sys.argv[1:])

    dbPath = "/visitor-db/visitor_db.db"
    backupPath = "/"

    startLogging("log/backup.log")

    logging.info(token)
    """
    dbx = dropbox.Dropbox(token)

    with open (dbPath, "rb") as dbFile:
        print "Backingup {0} to dropbox {1}".format(dbPath, backupPath)
        try:
            dbx.files_upload(dbFile.read(), backupPath, mode=WriteMode("overwrite"))
        except ApiError as err:
            if (err.error.is_path() and
                        err.error.get_path().reason.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()
    """

if __name__ == "__main__":
    main()
