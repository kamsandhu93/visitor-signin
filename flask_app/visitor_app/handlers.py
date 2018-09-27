import re

from flask import render_template, request
from visitor_app import app
from visitor_app import exceptions
from visitor_app import services


@app.route("/")
def view():
    return render_template("index.html")


@app.route("/status")
def status_handler():
    return "OK"


@app.route("/login", methods=["POST"])
def login_handler():
    try:
        validate_request_form_keys(request.form, valid_keys=["name", "surname", "visiting", "company"])
        validate_login_form_values(request.form)
        pass_id = services.login(request.form)
        app.logger.info("User logged in")

        return render_template("logedin.html", name=request.form["name"], pass_id=pass_id)
    except(exceptions.InvalidRequestBodyKeysEx, exceptions.InvalidRequestBodyValuesEx) as ex:
        app.log_exception(ex)
        return render_template("error.html"), 400
    except exceptions.DatabaseAccessEx as ex:
        app.log_exception(ex)
        return render_template("error.html"), 503
    except Exception as ex:
        app.logger.exception(ex)
        return render_template("error.html"), 500


@app.route("/logout", methods=["POST"])
def logout_handler():
    try:
        validate_request_form_keys(request.form, valid_keys=["pass_id"])
        validate_pass_id(request.form["pass_id"])
        full_name = services.logout(request.form)
        app.logger.info("User logged out")

        return render_template("logedout.html", first_name=full_name[0], surname=full_name[1])
    except(exceptions.InvalidRequestBodyKeysEx, exceptions.InvalidRequestBodyValuesEx) as ex:
        app.log_exception(ex)
        return render_template("error.html"), 400
    except exceptions.DatabaseAccessEx as ex:
        app.log_exception(ex)
        return render_template("error.html"), 503
    except Exception as ex:
        app.logger.exception(ex)
        return render_template("error.html"), 500


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

