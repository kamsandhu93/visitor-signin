from flask import Flask
from flask_cors import CORS

from shared.logger import init_logging
from shared.exception_handlers import register_generic_excpetion_handler, register_validation_exception_handler

app = Flask(__name__)
CORS(app)
app.config.from_pyfile("config.cfg")

init_logging(app, 'Print Service')
from printapi.handlers import status_handler, print_handler
register_generic_excpetion_handler(app)
register_validation_exception_handler(app)
