import logging
import ConfigParser
import argparse
import sys
import os
from visitor_app import app

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

def parseArgs(args):
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c", "--config",
        type=checkFile, required=False,
        help="Config file path"
    )

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

if __name__ == "__main__":

    arguments = parseArgs(sys.argv[1:])
    if arguments.config:
        config = parseConfig(arguments.config)
    else:
        config = {}

    logPath = os.path.join(config.get("LogDir", "./"), "flask.log")

    log_format = "%(asctime)s | Visitor_app | %(levelname)s | %(message)s"
    formatter = logging.Formatter(log_format)
    logger = logging.getLogger()

    file_handler = logging.FileHandler(logPath)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.DEBUG)

    app.logger.info("Starting visitor service")
    app.run(host=config.get("Host", "127.0.0.1"), port=int(config.get("Port", "5000")))
