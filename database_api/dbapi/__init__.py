import logging


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.cfg')

logPath = app.config["LOG_PATH"]

logFormat = "%(asctime)s | Database API | %(levelname)s | %(message)s"
formatter = logging.Formatter(logFormat)
logger = logging.getLogger()

fileHandler = logging.FileHandler(logPath)
fileHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
app.logger.addHandler(consoleHandler)

app.logger.setLevel(logging.DEBUG)

from dbapi.handlers import loginHandler, logoutHandler, statusHandler
