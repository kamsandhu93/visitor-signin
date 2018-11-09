# visitor-signin print
Print service of visitor signin system
## Project Dependencies

### Main Dependencies
 - Python 3
 - pip
 - CUPS

### Packages
 - [flask](http://flask.pocoo.org/)
 - [weasyprint](https://weasyprint.org/)
 - [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)
 - [qrcode[pil]](https://github.com/lincolnloop/python-qrcode)
 - [pycups](https://github.com/zdohnal/pycups)
 - [flask-cors](https://github.com/corydolphin/flask-cors)

## Infrastructure
The system is a flask application with a single POST endpoint `/print`.
The endpoint should receive a body with the following data structure:
```
{
    "passId": <string>,
    "name": <string>,
    "company": <string>
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

### Logging
Log location is `/printservice/log`. This is persisted to `/opt/visitorsignin/log` of the host

### Configuration
The flask application can be configured by setting environmental variables before running.
 - HOST - Host of flask application (default: 127.0.0.1)
 - PORT - Port of flask application (default: 5002)
 - LOG_PATH - Absolute path of log file (e.g. /printservice/log/print.log)
 - TEMPLATE_PATH - Absolute path of the template directory (e.g. /printservice/template)
