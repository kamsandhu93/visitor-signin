import re

from flask import render_template, request, jsonify
from visitor_app import app
from visitor_app import exceptions
from visitor_app import services

def createResponse(msg, status):
    return jsonify({'message': msg}), status

@app.route("/status")
def status_handler():
    return "OK"

#testing push
@app.route("/login", methods=["POST"])
def login_handler():
    try:
        request_form = request.get_json()['body']
        validate_request_form_keys(request_form, valid_keys=["name", "surname", "visiting", "company"])
        validate_login_form_values(request_form)
        pass_id = services.login(request_form)
        app.logger.info("User logged in")

        return jsonify({'passId': pass_id}), 200
    except(exceptions.InvalidRequestBodyKeysEx, exceptions.InvalidRequestBodyValuesEx) as ex:
        app.log_exception(ex)
        return createResponse("Missing or invalid request body", 400)
    except exceptions.DatabaseAccessEx as ex:
        app.log_exception(ex)
        return createResponse("Unable to access database", 503)
    except Exception as ex:
        app.logger.exception(ex)
        return createResponse("{0}".format(ex), 500)


@app.route("/logout", methods=["POST"])
def logout_handler():
    try:
        request.form = request.get_json()['body']
        validate_request_form_keys(request.form, valid_keys=["pass_id"])
        validate_pass_id(request.form["pass_id"])
        full_name = services.logout(request.form)
        app.logger.info("User logged out")

        response = {
            'firstName': full_name[0],
            'surname': full_name[1]
        }
        return jsonify(response), 200
    except(exceptions.InvalidRequestBodyKeysEx, exceptions.InvalidRequestBodyValuesEx) as ex:
        app.log_exception(ex)
        return createResponse("Missing or invalid request body", 400)
    except exceptions.DatabaseAccessEx as ex:
        app.log_exception(ex)
        return createResponse("Unable to access database", 503)
    except Exception as ex:
        app.logger.exception(ex)
        return createResponse("{0}".format(ex), 500)


def validate_request_form_keys(request_form, valid_keys):
    given_keys = list(request_form.keys())
    if given_keys != valid_keys:
        raise exceptions.InvalidRequestBodyKeysEx


def validate_login_form_values(request_form):
    regex = r"^[A-Za-z]{1,32}$"
    optional_fields = ['company']
    for key in request_form:
        if key not in optional_fields and not re.match(regex, request_form[key]):
            raise exceptions.InvalidRequestBodyValuesEx


def validate_pass_id(pass_id):
    regex = "^[0-9]{5}[a-z]$"
    if not re.match(regex, pass_id):
        raise exceptions.InvalidRequestBodyValuesEx
