import sys

from flask import request, jsonify
from backupapp import app
import backupapp.services as services

health = {
    "msg": "OK",
    "code": 200
}

if not services.runOperation("restore"):
    app.logger.error("Initial database restore failed")
    sys.exit()

@app.route("/status")
def statusHandler():
    return health["msg"], health["code"]

@app.route("/backup-online", methods=["POST"])
def backupHandler():
    if not services.runOperation("backup"):
        return jsonify({"Online Backup": "FAIL"}), 200
    return jsonify({"Backup": "OK"}), 200

@app.route("/backup-offline", methods=["POST"])
def backupHandler():
    if not services.runOperation("backupOffline")
        return jsonify({"Offline Backup": "FAIL"}), 200
    return jsonify({"Backup": "OK"}), 200

@app.route("/restore", methods=["POST"])
def restoreHandler():
    request_body = request.get_json()
    if request_body.get('forced'):
        if services.runOperation("restoreForce"):
            return jsonify({"Force restore": "OK"}), 200
        return jsonify({"Force restore": "FAIL"}), 500

    if services.runOperation("restore"):
        return jsonify({"Restore": "OK"}), 200
    return jsonify({"Restore": "FAIL"}), 500

def setHealth(msg, code):
    health['msg'] = msg
    health['code'] = code
