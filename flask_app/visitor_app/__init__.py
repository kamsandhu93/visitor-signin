import logging


from flask import Flask


app = Flask(__name__,
            template_folder = './templates',
            static_folder = './templates/static')
from visitor_app.handlers import catch_all, login_handler, logout_handler, status_handler

app.config.from_pyfile('config.cfg')

logPath = app.config["LOG_PATH"]

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
