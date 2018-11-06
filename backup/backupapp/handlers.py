import sys

from flask import request, jsonify
from backupapp import app
from backupapp.database import Database

status = {
    "msg": "OK",
    "code": 200
}

database = Database(app.config, app.logger)

if not database.runOperation("restore"):
    app.logger.error("Initial database restore failed")
    sys.exit()

@app.route("/status")
def statusHandler():
    return status["msg"], status["code"]

@app.route("/backup", methods=["POST"])
def backupHandler():
    backup = database.runOperation("backup")
    offlineBackup = database.runOperation("backupOffline")

    if not backup and not offlineBackup:
        status['msg'] = "ERROR"
        status['code'] = 500
        return "Backup FAIL", 500
    elif not backup or not offlineBackup:
        app.logger.warning("One of the backup service is down")
        status['msg'] = "WARNING"
        status['code'] = 200
        return "Backup WARNING", 200
    return "Backup OK", 200

@app.route("/restore", methods=["POST"])
def restoreHandler():
    request_body = request.get_json()
    if request_body.get('forced'):
        if database.runOperation("restoreForce"):
            return "Force restore OK", 200
        return "Force restore FAIL", 500

    if database.runOperation("restore"):
        return "Restore OK", 200
    return "Restore FAIL", 500
