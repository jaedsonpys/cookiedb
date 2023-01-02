# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

class DatabaseNotFoundError(Exception):
    def __init__(self, message):
        super().__init__(message)

    
class ItemNotExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DatabaseExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoOpenDatabaseError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDatabaseKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)
