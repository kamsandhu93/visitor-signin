import re

from flask import render_template, request, jsonify
from visitor_app import app
from visitor_app import exceptions
from visitor_app import services

def createResponse(msg, status):
    """
    create response
    """
    return jsonify({'message': msg}), status

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route("/status")
def status_handler():
    return "OK"

#testing push
@app.route("/login", methods=["POST"])
def login_handler():
    try:
        request.form = request.get_json()['body']
        validate_request_form_keys(request.form, valid_keys=["name", "surname", "visiting", "company"])
        validate_login_form_values(request.form)
        pass_id = services.login(request.form)
        app.logger.info("User logged in")

        responseMsg = "{0} {1} Signed in".format(request.form['name'], request.form['surname'])
        return createResponse(responseMsg, 200)
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

        responseMsg = "{0} {1} Signed out".format(full_name[0], full_name[1])
        return createResponse(responseMsg, 200)
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
    for value in list(request_form.values()):
        if not re.match(regex, value):
            raise exceptions.InvalidRequestBodyValuesEx


def validate_pass_id(pass_id):
    regex = "^[0-9]{5}[a-z]$"
    if not re.match(regex, pass_id):
        raise exceptions.InvalidRequestBodyValuesEx
