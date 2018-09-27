from visitor_app import app
from visitor_app import data_access


def login(request_form):
    pass_id = get_unique_pass_code()
    first_name = request_form["name"]
    surname = request_form["surname"]
    visiting = request_form["visiting"]

    data_access.log_visitor_in(pass_id, first_name, surname, visiting)

    ''' print pass'''

    return pass_id


def logout(request_form):
    pass_id = request_form["pass_id"]
    data_access.log_visitor_out(pass_id)
    full_name = data_access.get_visitor_full_name(pass_id)

    return full_name


def get_unique_pass_code():
    last_pass_id = data_access.get_last_pass_id()

    number = int(last_pass_id[:-1])
    if number == 99999:
        number = "00000"
        char = chr(ord(last_pass_id[-1]) + 1)
        pass_code = number + char
    else:
        number += 1
        char = last_pass_id[-1]
        pass_code = str(number).zfill(5) + char

    return pass_code
