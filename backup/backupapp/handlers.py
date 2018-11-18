import sys

from flask import request, jsonify
from backupapp import app
from backupapp.database import Database

health = {
    "msg": "OK",
    "code": 200
}

database = Database(app.config, app.logger)

if not database.runOperation("restore"):
    app.logger.error("Initial database restore failed")
    sys.exit()

@app.route("/status")
def statusHandler():
    return health["msg"], health["code"]

@app.route("/backup", methods=["POST"])
def backupHandler():
    backup = database.runOperation("backup")
    offlineBackup = database.runOperation("backupOffline")
    return backupStatus(backup, offlineBackup)

@app.route("/restore", methods=["POST"])
def restoreHandler():
    request_body = request.get_json()
    if request_body.get('forced'):
        if database.runOperation("restoreForce"):
            return jsonify({"Force restore": "OK"}), 200
        return jsonify({"Force restore": "FAIL"}), 500

    if database.runOperation("restore"):
        return jsonify({"Restore": "OK"}), 200
    return jsonify({"Restore": "FAIL"}), 500

def backupStatus(backup, offlineBackup):
    if not backup and not offlineBackup:
        setHealth("ERROR", 500)
        return jsonify({"Backup": "FAIL"}), 500
    elif not backup or not offlineBackup:
        app.logger.warning("One of the backup service is down")
        setHealth("WARNING", 200)
        return jsonify({"Backup": "WARNING"}), 200
    return jsonify({"Backup": "OK"}), 200

def setHealth(msg, code):
    health['msg'] = msg
    health['code'] = code
