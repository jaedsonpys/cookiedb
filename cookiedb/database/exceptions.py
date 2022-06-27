class DatabaseNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DatabaseExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)
