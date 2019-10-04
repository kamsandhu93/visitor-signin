from weasyprint import HTML
from bs4 import BeautifulSoup
from datetime import datetime

import qrcode
import cups
import time

from printapi import app


def print_pass(pass_data):
    name = pass_data["name"]
    pass_id = pass_data["passId"]
    # Because optional
    company = pass_data.get("company", "")
    generate_html_pass(name, company, pass_id)
    convert_html_pass_to_pdf()
    send_job_to_printer()


def generate_html_pass(name, company, pass_id):
    with open(app.config["PASS_TEMPLATE_PATH"], "r") as template:
        template_text = template.read()
        soup = BeautifulSoup(template_text, "html.parser")

    date = datetime.now().strftime("%d/%m/%Y")

    if app.config["ENABLE_QR"]:
        generate_qr(pass_id)

    append_text("name", name, soup)
    append_text("company", company, soup)
    append_text("date", "Date: {}".format(date), soup)
    append_text("passId", "Pass ID: {}".format(pass_id), soup)

    with open(app.config["GENERATED_HTML_PASS_PATH"], "w") as generated_pass:
        generated_pass.write(str(soup))

    app.logger.info("Generated pass with user={0} company={1} date={2} passId={3}".format(name,
                                                                                          company,
                                                                                          date,
                                                                                          pass_id))


def generate_qr(pass_id):
    img = qrcode.make(pass_id)
    img.save(pass_id)
    app.logger.info("Generated QR image with passId={0}".format(pass_id))


def append_text(identifier, text, soup):
    element = soup.find(id=identifier)
    element.append(text)
    app.logger.info("Replaced id={0} field with text={1}".format(identifier, text))


def convert_html_pass_to_pdf():
    HTML(app.config["GENERATED_HTML_PASS_PATH"]).write_pdf(app.config["PASS_PDF_PATH"])


def send_job_to_printer():
    conn = cups.Connection ()
    counter = 0
    printid = conn.printFile('Brother_QL-820NWB',app.config["PASS_PDF_PATH"],"",{})
    while printid in conn.getJobs():
        time.sleep(0.5)
        counter += 1
        if counter >= 20:
            raise UnableToPrintException("Print failed for user name={0} printid with passId={1}".format(name, pass_id))


class UnableToPrintException(Exception):
    pass
