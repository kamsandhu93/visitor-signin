import re

from flask import request, jsonify
from dbapi import app, exceptions, services

def createResponse(msg, status):
    return jsonify({'message': msg}), status

@app.route("/status")
def statusHandler():
    return "OK"

#testing push
@app.route("/login", methods=["POST"])
def loginHandler():
    try:
        requestBody = request.get_json()
        validateRequestBodyKeys(requestBody, validKeys=["name", "surname", "visiting", "company"])
        validateLoginRequestValues(requestBody)
        passId = services.login(requestBody)
        app.logger.info("User logged in")
        services.send_backup_request("online")
        services.send_backup_request("offline")

        return jsonify({'passId': passId}), 200
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
def logoutHandler():
    try:
        requestBody = request.get_json()
        validateRequestBodyKeys(requestBody, validKeys=["passId"])
        validatePassId(requestBody["passId"])
        fullName = services.logout(requestBody)
        app.logger.info("User logged out")

        services.sendBackupRequest("online")
        services.sendBackupRequest("offline")

        response = {
            'firstName': fullName[0],
            'surname': fullName[1]
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


def validateRequestBodyKeys(requestBody, validKeys):
    requestBodyKeys = list(requestBody.keys())
    if requestBodyKeys != validKeys:
        raise exceptions.InvalidRequestBodyKeysEx


def validateLoginRequestValues(requestBody):
    regex = {
        "name": r"^[A-Za-z]{1,32}$",
        "surname": r"^[A-Za-z]{1,32}$",
        "visiting": r"^[A-Za-z ]{1,32}$",
        "company": r"^[A-Za-z0-9 ]{1,32}$"
    }

    optionalKeys = ['company']

    for key in regex:
        if not re.match(regex[key], requestBody[key]):
            if key not in optionalKeys:
                raise exceptions.InvalidRequestBodyValuesEx
            if requestBody[key] and key in optionalKeys:
                raise exceptions.InvalidRequestBodyValuesEx

def validatePassId(passId):
    regex = "^[0-9]{5}[a-z]$"
    if not re.match(regex, passId):
        raise exceptions.InvalidRequestBodyValuesEx
