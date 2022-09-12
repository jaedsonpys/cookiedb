# CookieDB
# Copyright (C) 2022  Jaedson Silva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import os

from typing import Union
from datetime import datetime

from cryptography.fernet import Fernet


class JSONHandler:
    def __init__(
        self,
        enc_key: Union[bytes, str],
        database_local: str
    ):
        self._fernet = Fernet(enc_key)
        self._document_local = database_local

    @staticmethod
    def _save_file(file_content: str, filepath: str) -> None:
        with open(filepath, 'w') as writer:
            writer.write(file_content)

    def exists_document(self, database: str) -> bool:
        document_path = os.path.join(self._document_local, database + '.cookiedb')
        return os.path.isfile(document_path)

    def encrypt_json(self, obj: dict) -> str:
        dict_str = json.dumps(obj)
        encrypted_dict = self._fernet.encrypt(dict_str.encode())
        return encrypted_dict.decode()

    def decrypt_json(self, encrypted: bytes) -> dict:
        decrypted_json = self._fernet.decrypt(encrypted)
        json_data = json.loads(decrypted_json)
        return json_data

    def create_document(self, name: str) -> dict:
        document_path = os.path.join(self._document_local, name + '.cookiedb')
        created_time = str(datetime.now().replace(microsecond=0))

        document = {
            'name': name,
            'created_at': created_time,
            'updated_at': created_time,
            'items': {}
        }

        encrypted_data = self.encrypt_json(document)
        self._save_file(encrypted_data, document_path)

        return document

    def get_document(self, database: str) -> Union[None, dict]:
        document_path = os.path.join(self._document_local, database + '.cookiedb')

        try:
            with open(document_path, 'rb') as reader:
                encrypted_data = reader.read()
        except FileNotFoundError:
            document = None
        else:
            document = self.decrypt_json(encrypted_data)

        return document

    def update_document(self, database: str, items: dict):
        document_path = os.path.join(self._document_local, database + '.cookiedb')

        document = self.get_document(database)
        update_time = datetime.now().replace(microsecond=0)

        document['items'] = items
        document['updated_at'] = str(update_time)

        encrypted_json = self.encrypt_json(document)
        self._save_file(encrypted_json, document_path)
