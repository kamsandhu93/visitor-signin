class PrintError(Exception):
    def __init__(self, message):
        super(PrintError, self).__init__(message)
