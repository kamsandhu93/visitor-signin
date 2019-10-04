from flask import jsonify
from flask import current_app as app

from shared. utilities import RequestValidationException

#todo use current_app rather than egister metjhods
def register_generic_excpetion_handler(app):
    app.register_error_handler(Exception, generic_exception_handler)

@app.err(Exception)
def generic_exception_handler(ex):
    app.logger.exception(ex)
    return jsonify("Internal Server Error"), 500


def register_validation_exception_handler(app):
    app.register_error_handler(RequestValidationException, validation_error_handler)


def validation_error_handler(ex):
    app.log_exception(ex)
    return jsonify("Bad Request"), 400
