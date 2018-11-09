import logging
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.cfg')
from printapi.handlers import statusHandler, printHandler

logPath = app.config["LOG_PATH"]

logFormat = "%(asctime)s | PrintService | %(levelname)s | %(message)s"
formatter = logging.Formatter(logFormat)

fileHandler = logging.FileHandler(logPath)
fileHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
app.logger.addHandler(consoleHandler)

app.logger.setLevel(logging.DEBUG)
