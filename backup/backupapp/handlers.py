from flask import request, jsonify
from backupapp import app
import backupapp.services as services

health = {
    "msg": "OK",
    "code": 200
}

@app.route("/status")
def status_handler():
    return health["msg"], health["code"]

@app.route("/backup-online", methods=["POST"])
def online_backup_handler():
    try:
        services.backup()
        return jsonify({"Online Backup": "OK"}), 200
    except Exception as ex:
        app.logger.error("backup-online operation failed")
        app.log_exception(ex)
        health["msg"] = "Latest backup-online operation failed"
        health["code"] = 500
        return jsonify({"Online Backup": "FAIL"}), 500



@app.route("/backup-offline", methods=["POST"])
def offline_backup_handler():
    try:
        services.backup_offline()
        return jsonify({"Offline Backup": "OK"}), 200
    except Exception as ex:
        app.logger.error("backup-offline operation failed")
        app.log_exception(ex)
        health["msg"] = "Latest backup-offline operation failed"
        health["code"] = 500
        return jsonify({"Offline Backup": "FAIL"}), 500
