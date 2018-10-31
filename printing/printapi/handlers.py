from printapi import app
from printapi.exceptions import PrintError

from weasyprint import HTML
from bs4 import BeautifulSoup
from datetime import datetime

from flask import request, jsonify

import subprocess
import os
import qrcode

templatePath = app.config['TEMPLATE_PATH']

passTemplate = os.path.join(templatePath, "template.html")
generatedPass = os.path.join(templatePath, "generated.html")
qrImage = os.path.join(templatePath, "qr.png")
pdfToPrint = os.path.join(templatePath, "passToPrint.pdf")

@app.route("/status")
def statusHandler():
    return "OK"

@app.route("/print", methods=["POST"])
def printHandler():
    try:
        app.logger.info("Received printing request")
        passData = request.get_json()['body']
        generatePass(passData)
        convertToPdf()
        return printPass()
    except PrintError as e:
        app.log_exception(e)
        return "Printing failed with error: {0}".format(e), 500
    except Exception as e:
        app.log_exception(e)
        return e, 500

def generatePass(passData):
    with open(passTemplate, "r") as template:
        template_text = template.read()
        soup = BeautifulSoup(template_text, 'html.parser')

    passId = passData['passId']
    date = datetime.now().strftime("%d/%m/%Y")

    generateQr(passId)
    appendText("name", passData['name'], soup)
    appendText("company", passData['company'], soup)
    appendText("date", "Date: {}".format(date), soup)
    appendText("passId", "Pass ID: {}".format(passId), soup)

    with open(generatedPass, "w") as gen_pass:
        gen_pass.write(str(soup))

    app.logger.info("Generated pass with user={0} company={1} date={2} passId={3}".format(passData['name'], passData['company'], date, passId))

def generateQr(passId):
    img = qrcode.make(str(passId))
    img.save(qrImage)
    app.logger.info("Generated QR image with passId={0}".format(passId))

def appendText(id, text, soup):
    element = soup.find(id=id)
    element.append(text)
    app.logger.info("Replaced id={0} field with text={1}".format(id, text))

def convertToPdf():
    HTML(generatedPass).write_pdf(pdfToPrint)

def printPass():
    bashCommand = "lp {0}".format(pdfToPrint)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise PrintError(error)
    return output, 200
