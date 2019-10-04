import re


def validate_request_body_values(request_body, regex):
    for key, value in request_body.items():
        if not re.match(regex[key], value):
            raise RequestValidationException("Invalid value: {0} for key: {1}".format(value, key))


def validate_request_body_keys(request_body, valid_keys, optional_keys=[]):
    request_body_keys = list(request_body.keys())

    for key in valid_keys:
        if key not in request_body_keys:
            raise RequestValidationException("Missing key: {0}".format(key))

    for key in request_body_keys:
        if key not in valid_keys and key not in optional_keys:
            raise RequestValidationException("Unexpected key: {0}".format(key))


class RequestValidationException(Exception):
    pass
