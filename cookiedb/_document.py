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

import pickle
from typing import Union

from . import exceptions
from ._encrypt import Cryptography


class Document:
    def __init__(self, cryptography: Cryptography, document_path: str) -> None:
        self._crypt = cryptography
        self._document_path = document_path

    @staticmethod
    def _save_file(file_content: str, filepath: str) -> None:
        with open(filepath, 'wb') as writer:
            writer.write(file_content)

    def _encrypt(self, obj: dict) -> str:
        pickle_file = pickle.dumps(obj)
        encrypted_data = self._crypt.encrypt(pickle_file)
        return encrypted_data

    def _decrypt(self, encrypted: bytes) -> dict:
        decrypted_data = self._crypt.decrypt(encrypted)
        data = pickle.loads(decrypted_data)
        return data

    def create_document(self) -> dict:
        document = {
            'items': {}
        }

        data = self._encrypt(document)
        self._save_file(data, self._document_path)
        return document

    def get_document(self) -> Union[None, dict]:
        try:
            with open(self._document_path, 'rb') as reader:
                data = reader.read()
        except FileNotFoundError:
            raise exceptions.DatabaseNotFoundError(f'Database "{self._document_path}" not found')
        else:
            document = self._decrypt(data)

        return document

    def update_document(self, items: dict) -> None:
        document = self.get_document()
        document['items'] = items
        encrypted_json = self._encrypt(document)
        self._save_file(encrypted_json, self._document_path)
