from flask import request, jsonify
from printapi import app, services
from shared.utilities import validate_request_body_keys, validate_request_body_values

REQUEST_VALIDATION_REGEX = {
    "name": r"^[A-Za-z ]{1,64}$",
    "company": r"^[A-Za-z0-9 ]{1,32}$",
    "passId": r"^[0-9]{5}[a-z]$"
}


@app.route("/status")
def status_handler():
    return jsonify("OK"), 200


@app.route("/print", methods=["POST"])
def print_handler():
    app.logger.info("Received printing request")
    request_body = request.get_json()
    validate_request_body_keys(request_body, valid_keys=["name", "passId"], optional_keys=["company"])
    validate_request_body_values(request_body, REQUEST_VALIDATION_REGEX)
    services.print_pass(request_body)

    return jsonify("OK"), 200


@app.errorhandler(services.UnableToPrintException)
def unable_to_print_error_handler(ex):
    app.log_exception(ex)
    return jsonify("Service Unavailable"), 503
