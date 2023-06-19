# Copyright 2023 Jaedson Silva
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class ItemNotExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ItemIsNotAListError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DatabaseExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidDatabaseKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidKeyError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidTokenError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidSignatureError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
