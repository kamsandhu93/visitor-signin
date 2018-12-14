import re

from flask import request, jsonify
from printapi import app, services, exceptions


@app.route("/status")
def status_handler():
    return jsonify("OK"), 200


@app.route("/print", methods=["POST"])
def print_handler():
    try:
        app.logger.info("Received printing request")
        request_body = request.get_json()
        validate_request_body_keys(request_body, valid_keys=["name", "passId"], optional_keys=["company"])
        validate_request_body_values(request_body)
        services.print_pass(request_body)

        return jsonify("OK"), 200
    except exceptions.UnableToPrintException as e:
        app.log_exception(e)
        return jsonify("Service Unavailable"), 503
    except(exceptions.InvalidRequestBodyKeysException, exceptions.InvalidRequestBodyValuesException):
        return jsonify("Bad Request"), 400
    except Exception as e:
        app.log_exception(e)
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
        "name": r"^[A-Za-z ]{1,64}$",
        "company": r"^[A-Za-z0-9 ]{1,32}$",
        "passId": r"^[0-9]{5}[a-z]$"
    }

    for key, value in request_body.items():
        if not re.match(regex[key], value):
            raise exceptions.InvalidRequestBodyValuesException("Invalid value: {0} for key: {1}".format(value, key))
