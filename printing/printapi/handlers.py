from printapi import app, services, exceptions
from flask import request, jsonify



@app.route("/status")
def status_handler():
    return "OK", 200

@app.route("/print", methods=["POST"])
def print_handler():
    try:
        app.logger.info("Received printing request")
        pass_data = request.get_json()
        services.print_pass(pass_data)

        return jsonify("OK"), 200
    except exceptions.UnableToPrintException as e:
        app.log_exception(e)
        return "Service Unavailable", 503
    except Exception as e:
        app.log_exception(e)
        return "Unknown Server Error", 500


