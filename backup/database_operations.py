import sys
import configparser
import argparse
import logging
import time
import os

from database import Database

def main():
    arguments = parse_args(sys.argv[1:])
    config = parse_config(arguments.configPath)
    start_logging(config, arguments.operationType)
    database = Database(config)
    run_database_operation(database, arguments.operationType, arguments.isService)

def parse_args(args):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config", dest="configPath",
        type=checkFile, required=False,
        default="/backupservice/database_operations.cfg",
        help="Config file path"
    )

    parser.add_argument(
        "-o", "--operation", dest="operationType",
        type=checkOperation, required=True,
        help="Backup or restore database"
    )

    parser.add_argument(
        "-s", "--service",
        dest="isService", action="store_true",
        help="Run script continuously as a service"
    )

    parser.set_defaults(isService=False)

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

def parse_config(configPath):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(configPath)

    return config.defaults()

def start_logging(config, operation):
    logFilePath = os.path.join(config["LogDir"], "backup.log")
    loggingFormat = logging.Formatter("%(asctime)s | {0} | %(levelname)s | %(message)s".format(operation))

    fileHandler = logging.FileHandler(logFilePath, encoding = "utf-8")
    fileHandler.setFormatter(loggingFormat)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(loggingFormat)

    logging.root.setLevel(logging.INFO)
    logging.root.addHandler(fileHandler)
    logging.root.addHandler(consoleHandler)

def run_database_operation(database, operationType, isService):
    if isService:
        rune_database_operation_as_service(database, operationType)
    else:
        database.run_operation(operationType)

def rune_database_operation_as_service(database, operationType):
    currentHash = {}
    while True:
        newHash = database.get_hash()
        if newHash != currentHash:
            database.run_operation(operationType)
            currentHash = newHash
        time.sleep(30)

if __name__ == "__main__":
    main()
