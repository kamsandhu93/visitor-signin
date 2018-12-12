import requests
from dbapi import app, data_access


def login(requestBody):
    passId = generatePassId()
    firstName = requestBody["name"]
    surname = requestBody["surname"]
    visiting = requestBody["visiting"]
    company = requestBody["company"]

    data_access.logVisitorIn(passId, firstName, surname, visiting, company)

    return passId


def logout(requestBody):
    passId = requestBody["passId"]
    data_access.logVisitorOut(passId)
    fullName = data_access.getVisitorFullName(passId)

    return fullName


def generatePassId():
    lastPassId = data_access.getLastPassId()

    number = int(lastPassId[:-1])
    if number == 99999:
        number = "00000"
        char = chr(ord(lastPassId[-1]) + 1)
        passId = number + char
    else:
        number += 1
        char = lastPassId[-1]
        passId = str(number).zfill(5) + char

    data_access.updateLastPassId(passId)

    return passId


def sendBackupRequest(backup_type):
    try:
        url = "http://{0}:5004/backup-{1}".format(app.config["REQUEST_HOST"], backup_type)
        requests.post(url)
    except Exception as e:
        app.logger.warning(e)
