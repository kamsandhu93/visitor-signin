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
        validate_request_body_keys(request_body, valid_keys=["name", "company", "passID"])
        validate_request_body_values(request_body)
        services.print_pass(request_body)

        return jsonify("OK"), 200
    except exceptions.UnableToPrintException as e:
        app.log_exception(e)
        return jsonify("Service Unavailable"), 503
    except Exception as e:
        app.log_exception(e)
        return jsonify("Unknown Server Error"), 500


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
        "company": r"^[A-Za-z0-9 ]{1,32}$",
        "passID": r"^[0-9]{5}[a-z]$"
    }

    for key, value in request_body.items():
        if not re.match(regex[key], value):
            raise exceptions.InvalidRequestBodyValuesEx
