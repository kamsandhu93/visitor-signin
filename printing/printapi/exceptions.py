class UnableToPrintException(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class InvalidRequestBodyKeysEx(Exception):
    def __init__(self, message=""):
        super().__init__(message)


class InvalidRequestBodyValuesEx(Exception):
    def __init__(self, message=""):
        super().__init__(message)