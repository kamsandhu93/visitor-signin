import re

from flask import request, jsonify
from backupapp import app
from backupapp.database import Database

status = {
    "msg": "OK",
    "code": 200
}

def createResponse(msg, status):
    return jsonify({'message': msg}), status

database = Database(config)

@app.route("/status")
def status_handler():
    return status["msg"], status["code"]

@app.route("/backup", methods=["POST"])
def backup_handler():
    

@app.route("/restore", methods=["POST"])
def restore_handler():
