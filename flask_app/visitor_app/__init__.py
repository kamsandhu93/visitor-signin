from flask import Flask

app = Flask(__name__)

from flask_app.visitor_app.handlers import view, login_handler, logout_handler




