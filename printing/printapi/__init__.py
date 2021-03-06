import logging
from flask import Flask
from flask_cors import CORS
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app)
app.config.from_pyfile("config.cfg")
from printapi.handlers import status_handler, print_handler

app.logger.removeHandler(default_handler)

log_path = app.config["LOG_PATH"]
log_format = "%(asctime)s | Print Service | %(levelname)s | %(message)s"
formatter = logging.Formatter(log_format)


file_handler = RotatingFileHandler(log_path, maxBytes=5242880, backupCount=5)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)

app.logger.setLevel(logging.DEBUG)
