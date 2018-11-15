import logging


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.cfg')

log_path = app.config["LOG_PATH"]
log_format = "%(asctime)s | Database API | %(levelname)s | %(message)s"
formatter = logging.Formatter(log_format)
logger = logging.getLogger()

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(formatter)
app.logger.addHandler(consoleHandler)

app.logger.setLevel(logging.DEBUG)

from dbapi.handlers import login_handler, logout_handler, status_handler
