# visitor-signin print
Print service of visitor signin system
## Project Dependencies

### Main Dependencies
 - Python 3
 - pip
 - CUPS

### Packages
 - flask
 - weasyprint
 - beautifulsoup4
 - qrcode[pil]
 - pycups
 - flask-cors

## Infrastructure
The system is a flask application with a single POST endpoint `/print`.
The endpoint should receive a body with the following data structure:
```
{
    "passId": "00045a",
    "name": "Test User",
    "company": "A Company"
}
```
### Pass PDF generation
The pass template is a html file with empty name, company, passId, date and qr fields.
Using beautifulsoup4, the values from the POST request are substituted in to their respective places in `template/template.html`. This generates `template/generated.html`.
The `qr.png` used by the template is generated using qrcode[pil].
The full template is then converted to pdf via weasyprint.

### Pass Printing
Python sends `lp <document>` command to bash. `lp` command prints to the default cups printer. Printing will fail if no default printer is set.
When printing from container, `start.sh` adds the host IP address to `/etc/cups/client.conf`. This allows the cups server in the container to connect to the cups server on the host. The `lp` command will send print jobs to the default printer on the host instead.
