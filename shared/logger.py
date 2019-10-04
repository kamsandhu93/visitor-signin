import logging

from flask.logging import default_handler
from logging.handlers import RotatingFileHandler


def init_logging(app, service_name):
    app.logger.removeHandler(default_handler)

    log_path = app.config["LOG_PATH"]
    log_format = "%(asctime)s | {} | %(levelname)s | %(message)s".format(service_name)
    formatter = logging.Formatter(log_format)

    file_handler = RotatingFileHandler(log_path, maxBytes=5242880, backupCount=5)
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.setLevel(logging.DEBUG)
