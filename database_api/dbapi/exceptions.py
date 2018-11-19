class InvalidRequestBodyKeysEx(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class InvalidRequestBodyValuesEx(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class DatabaseAccessEx(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class DatabaseBackupException(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class AlreadyLoggedOutException(Exception):
    def __init__(self, message=""):
        super().__init__(message)