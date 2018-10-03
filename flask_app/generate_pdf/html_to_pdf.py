from datetime import datetime
# ToDo review security for the following packages
from bs4 import BeautifulSoup


def generate_pass(pass_id, name, company=None):
    """
    generates a pdf pass to print in (the same directory) test.pdf

    Args:
        pass_id(string):
        name(string):
        company(string): optional

    """
    with open("./generate_pdf/template.html") as template:
        txt = template.read()
        soup = BeautifulSoup(txt)

    name_element = soup.find(id="name")
    name_element.string.replace_with(name)
    company_element = soup.find(id="company")
    company_element.string.replace_with(company)
    date_element = soup.find(id="date")
    # ToDO do we need to pick this date from the DB ? or something 
    date_element.string.replace_with(datetime.now().strftime("%d-%m-%Y"))
    pass_id_element = soup.find(id="passid")
    pass_id_element.string.replace_with(pass_id_element.string + pass_id)

    with open("./generate_pdf/generated.html", "w") as out:
        out.write(str(soup))

    import pdfkit

    class HeadlessPdfKit(pdfkit.PDFKit):
        def command(self, path=None):
            return ['xvfb-run', '--'] + super().command(path)

    with open("./generate_pdf/generated.html") as generated:
        txt = generated.read()
        pdf = HeadlessPdfKit(txt, 'string').to_pdf(False)
        f = open('lol.pdf', 'w+b')
        f.write(pdf)
    # pdf_options = {
    #     'page-size':'A4',
    #     'margin-top':'0cm',
    #     'margin-bottom':'0cm',
    #     'margin-left':'0cm',
    #     'margin-right':'0cm'
    # }
    # pdfkit.from_file('./generate_pdf/generated.html', 'test.pdf', options=pdf_options)
    # import imgkit
    # imgkit.from_file('generated.html', 'out.jpg', options={"xvfb": "", "quality":100})