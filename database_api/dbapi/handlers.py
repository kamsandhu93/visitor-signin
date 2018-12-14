import re
import sqlite3

from flask import request, jsonify
from dbapi import app, exceptions, services


@app.route("/status")
def status_handler():
    return jsonify("OK"), 200


@app.route("/login", methods=["POST"])
def login_handler():
    try:
        app.logger.info("Login request received")
        request_body = request.get_json()
        validate_request_body_keys(request_body, valid_keys=["name", "surname", "visiting"], optional_keys=["company"])
        validate_request_body_values(request_body)
        pass_id = services.login(request_body)
        app.logger.info("User logged in: {}".format(pass_id))

        services.send_backup_request("online")
        services.send_backup_request("offline")

        return jsonify({"passId": pass_id}), 200
    except(exceptions.InvalidRequestBodyKeysException, exceptions.InvalidRequestBodyValuesException) as ex:
        app.log_exception(ex)
        return jsonify("Bad Request"), 400
    except sqlite3.Error as ex:
        app.log_exception(ex)
        return jsonify("Service Unavailable"), 503
    except Exception as ex:
        app.logger.exception(ex)
        return jsonify("Internal Server Error"), 500


@app.route("/logout", methods=["POST"])
def logout_handler():
    try:
        app.logger.info("Logout request received")
        request_body = request.get_json()
        validate_request_body_keys(request_body, valid_keys=["passId"])
        validate_request_body_values(request_body)
        full_name = services.logout(request_body)
        app.logger.info("User logged out: {} {}".format(full_name, request_body["passId"]))

        services.send_backup_request("online")
        services.send_backup_request("offline")


        response = {
            "firstName": full_name[0],
            "surname": full_name[1]
        }

        return jsonify(response), 200
    except(exceptions.InvalidRequestBodyKeysException, exceptions.InvalidRequestBodyValuesException) as ex:
        app.log_exception(ex)
        return jsonify("Bad Request"), 400
    except exceptions.AlreadyLoggedOutException as ex:
        app.log_exception(ex)
        return jsonify("Conflict"), 409
    except sqlite3.Error as ex:
        app.log_exception(ex)
        return jsonify("Service Unavailable"), 503
    except Exception as ex:
        app.logger.exception(ex)
        return jsonify("Internal Server Error"), 500


def validate_request_body_keys(request_body, valid_keys, optional_keys=[]):
    request_body_keys = list(request_body.keys())

    for key in valid_keys:
        if key not in request_body_keys:
            raise exceptions.InvalidRequestBodyKeysException("Missing key: {0}".format(key))

    for key in request_body_keys:
        if key not in valid_keys and key not in optional_keys:
            raise exceptions.InvalidRequestBodyKeysException("Unexpected key: {0}".format(key))


def validate_request_body_values(request_body):
    regex = {
        "name": r"^[A-Za-z]{1,32}$",
        "surname": r"^[A-Za-z]{1,32}$",
        "visiting": r"^[A-Za-z ]{1,32}$",
        "company": r"^[A-Za-z0-9 ]{1,32}$",
        "passId": r"^[0-9]{5}[a-z]$"
    }

    for key, value in request_body.items():
        if not re.match(regex[key], value):
            raise exceptions.InvalidRequestBodyValuesException("Invalid value: {0} for key: {1}".format(value, key))


