from datetime import datetime

# ToDo review security for the following packages
import pdfkit
from bs4 import BeautifulSoup


def generate_pass(name, company=None):
    """
    generates a pdf pass to print in (the same directory) test.pdf 

    Args:
        name(string):
        company(string): optional

    Returns:
        pass_id(string)
    """
    # ToDo generate a random/consecutive numbers
    pass_id = "0001"

    with open("template.html") as template:
        txt = template.read()
        soup = BeautifulSoup(txt)

    name_element = soup.find(id="name")
    name_element.string.replace_with(name)
    company_element = soup.find(id="company")
    company_element.string.replace_with(company)
    date_element = soup.find(id="date")
    date_element.string.replace_with(datetime.now().strftime("%d-%M-%Y"))
    pass_id_element = soup.find(id="passid")
    pass_id_element.string.replace_with(pass_id_element.string + pass_id)

    with open("generated.html", "w") as out:
        out.write(str(soup))


    pdf_options = {
        'page-size':'A4',
        'encoding':'utf-8', 
        'margin-top':'0cm',
        'margin-bottom':'0cm',
        'margin-left':'0cm',
        'margin-right':'0cm'
    }
    pdfkit.from_file('generated.html', 'test.pdf', options=pdf_options)

    return pass_id