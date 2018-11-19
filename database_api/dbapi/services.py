import requests

from dbapi import app, data_access, exceptions


def login(request_body):
    pass_id = generate_pass_id()
    first_name = request_body["name"]
    surname = request_body["surname"]
    visiting = request_body["visiting"]
    # Because optional
    company = request_body.get('company', None)

    data_access.log_visitor_in(pass_id, first_name, surname, visiting, company)

    return pass_id


def logout(request_body):
    pass_id = request_body["passId"]
    time_out = data_access.get_logout_time(pass_id)
    if time_out[0] is not None:
        raise exceptions.AlreadyLoggedOutException

    data_access.log_visitor_out(pass_id)
    full_name = data_access.get_visitor_full_name(pass_id)

    return full_name


def generate_pass_id():
    last_pass_id = data_access.get_last_pass_id()

    number = int(last_pass_id[:-1])
    if number == 99999:
        number = "00000"
        char = chr(ord(last_pass_id[-1]) + 1)
        pass_id = number + char
    else:
        number += 1
        char = last_pass_id[-1]
        pass_id = str(number).zfill(5) + char

    data_access.update_last_pass_id(pass_id)

    return pass_id


def send_backup_request():
        try:
            url = app.config["BACKUP_ENDPOINT"]
            request = requests.post(url)

            if request.status_code != 200:
                raise exceptions.DatabaseBackupException

        except Exception as e:
            app.logger.warn(e)
