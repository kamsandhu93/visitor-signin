from flask import Flask

app = Flask(__name__)

from visitor_app.handlers import view, login_handler, logout_handler




