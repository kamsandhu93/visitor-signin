import sqlite3

from flask import request, jsonify
from dbapi import app, services
from shared.utilities import validate_request_body_values, validate_request_body_keys


REQUEST_VALIDATION_REGEX = {
    "name": r"^[A-Za-z]{1,32}$",
    "surname": r"^[A-Za-z]{1,32}$",
    "visiting": r"^[A-Za-z ]{1,32}$",
    "company": r"^[A-Za-z0-9 ]{1,32}$",
    "passId": r"^[0-9]{5}[a-z]$"
}


@app.route("/status")
def status_handler():
    return jsonify("OK"), 200


@app.route("/login", methods=["POST"])
def login_handler():
    app.logger.info("Login request received")
    request_body = request.get_json()
    validate_request_body_keys(request_body, valid_keys=["name", "surname", "visiting"], optional_keys=["company"])
    validate_request_body_values(request_body, REQUEST_VALIDATION_REGEX)
    pass_id = services.login(request_body)
    app.logger.info("User logged in: {}".format(pass_id))

    return jsonify({"passId": pass_id}), 200


@app.route("/logout", methods=["POST"])
def logout_handler():
    app.logger.info("Logout request received")
    request_body = request.get_json()
    validate_request_body_keys(request_body, valid_keys=["passId"])
    validate_request_body_values(request_body, REQUEST_VALIDATION_REGEX)
    full_name = services.logout(request_body)
    app.logger.info("User logged out: {} {}".format(full_name, request_body["passId"]))

    response = {
        "firstName": full_name[0],
        "surname": full_name[1]
    }

    return jsonify(response), 200


@app.errorhandler(sqlite3.Error)
def database_error_handler(ex):
    app.log_exception(ex)
    return jsonify("Service Unavailable"), 503


@app.errorhandler(services.AlreadyLoggedOutException)
def already_logged_out_error_handler(ex):
    app.log_exception(ex)
    return jsonify("Conflict"), 409
