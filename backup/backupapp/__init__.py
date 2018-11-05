import logging


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
from backupapp.handlers import backup_handler, restore_handler, status_handler

app.config.from_pyfile('config.cfg')

log_path = app.config["LOG_PATH"]

log_format = "%(asctime)s | Backup | %(levelname)s | %(message)s"
formatter = logging.Formatter(log_format)
logger = logging.getLogger()

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
app.logger.addHandler(console_handler)

app.logger.setLevel(logging.DEBUG)
