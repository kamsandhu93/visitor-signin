import re

from flask import request, jsonify
from dbapi import app, exceptions, services


@app.route("/status")
def status_handler():
    return jsonify("OK"), 200


@app.route("/login", methods=["POST"])
def login_handler():
    try:
        request_body = request.get_json()
        validate_request_body_keys(request_body, valid_keys=["name", "surname", "visiting"], optional_keys=["company"])
        validate_request_body_values(request_body)
        pass_id = services.login(request_body)
        app.logger.info("User logged in")
        services.send_backup_request()

        return jsonify({"passId": pass_id}), 200
    except(exceptions.InvalidRequestBodyKeysEx, exceptions.InvalidRequestBodyValuesEx) as ex:
        app.log_exception(ex)
        return jsonify("Bad Request", 400)
    except exceptions.DatabaseAccessEx as ex:
        app.log_exception(ex)
        return jsonify("Service Unavailable", 503)
    except Exception as ex:
        app.logger.exception(ex)
        return jsonify("Internal Server Error", 500)


@app.route("/logout", methods=["POST"])
def logout_handler():
    try:
        request_body = request.get_json()
        validate_request_body_keys(request_body, valid_keys=["passId"])
        validate_request_body_values(request_body)
        full_name = services.logout(request_body)
        app.logger.info("User logged out")

        services.send_backup_request()  #TODO should this be here

        response = {
            "firstName": full_name[0],
            "surname": full_name[1]
        }

        return jsonify(response), 200
    except(exceptions.InvalidRequestBodyKeysEx, exceptions.InvalidRequestBodyValuesEx) as ex:
        app.log_exception(ex)
        return jsonify("Bad Request", 400)
    except exceptions.DatabaseAccessEx as ex:
        app.log_exception(ex)
        return jsonify("Service Unavailable", 503)
    except Exception as ex:
        app.logger.exception(ex)
        return jsonify("Internal Server Error", 500)


def validate_request_body_keys(request_body, valid_keys, optional_keys=[]):
    request_body_keys = list(request_body.keys())

    for key in valid_keys:
        if key not in request_body_keys:
            raise exceptions.InvalidRequestBodyKeysEx

    for key in request_body_keys:
        if key not in valid_keys or key not in optional_keys:
            raise exceptions.InvalidRequestBodyKeysEx


def validate_request_body_values(request_body):
    regex = {
        "name": r"^[A-Za-z]{1,32}$",
        "surname": r"^[A-Za-z]{1,32}$",
        "visiting": r"^[A-Za-z ]{1,32}$",
        "company": r"^[A-Za-z0-9 ]{1,32}$",
        "passID": r"^[0-9]{5}[a-z]$"
    }

    for key, value in request_body.items():
        if not re.match(regex[key], value):
            raise exceptions.InvalidRequestBodyValuesEx


