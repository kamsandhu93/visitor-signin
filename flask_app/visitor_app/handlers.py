from flask import render_template, request
from visitor_app import app
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
        validate_login_form_keys(request.form)
        validate_login_form_values(request.form)
        pass_id = services.login(request.form)
        app.logger.info("User logged in")
        return render_template("logedin.html", name=request.form["name"], pass_id=pass_id)
    except Exception as ex:
        return render_template("error.html"), 500


@app.route("/logout", methods=["POST"])
def logout_handler():
    try:
        validate_logout_form_keys(request.form)
        validate_pass_id(request.form["pass_id"])
        full_name = services.logout(request.form)
        app.logger.info("User logged in")
        return render_template("logedout.html", first_name=full_name[0], surname=full_name[1])
    except Exception as ex:
        app.logger.exception(ex)
        return render_template("error.html"), 500

def validate_login_form_keys(request_form):
    valid_keys = ["name", "first_name", "visiting"]
    pass

def validate_logout_form_keys(request_form):
    valid_keys = ["pass_id"]
    pass

def validate_login_form_values(request_form):
    pass

def validate_pass_id(pass_id):
    pass

