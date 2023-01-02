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

import os
from datetime import datetime
from typing import Union

import pickle
from cryptography import fernet

from . import exceptions


class Document:
    def __init__(self, key: bytes, database_local: str) -> None:
        self._fernet = fernet.Fernet(key)
        self._document_local = database_local
        self._key = key.decode()

    @staticmethod
    def _save_file(file_content: str, filepath: str) -> None:
        with open(filepath, 'wb') as writer:
            writer.write(file_content)

    def exists_document(self, database: str) -> bool:
        document_path = os.path.join(self._document_local, database + '.cookiedb')
        return os.path.isfile(document_path)

    def _encrypt(self, obj: dict) -> str:
        pickle_file = pickle.dumps(obj)
        encrypted_data = self._fernet.encrypt(pickle_file)
        return encrypted_data

    def _decrypt(self, encrypted: bytes) -> dict:
        decrypted_data = self._fernet.decrypt(encrypted)
        data = pickle.loads(decrypted_data)
        return data

    def create_document(self, name: str) -> dict:
        document_path = os.path.join(self._document_local, name + '.cookiedb')
        created_time = str(datetime.now().replace(microsecond=0))

        document = {
            'name': name,
            'created_at': created_time,
            'updated_at': created_time,
            'items': {}
        }

        data = self._encrypt(document)
        self._save_file(data, document_path)

        return document

    def get_document(self, database: str) -> Union[None, dict]:
        document_path = os.path.join(self._document_local, database + '.cookiedb')

        try:
            with open(document_path, 'rb') as reader:
                data = reader.read()
        except FileNotFoundError:
            raise exceptions.DatabaseNotFoundError(f'Database "{database}" not found')
        else:
            document = self._decrypt(data)

        return document

    def update_document(self, database: str, items: dict) -> None:
        document_path = os.path.join(self._document_local, database + '.cookiedb')

        document = self.get_document(database)
        update_time = datetime.now().replace(microsecond=0)

        document['items'] = items
        document['updated_at'] = str(update_time)

        encrypted_json = self._encrypt(document)
        self._save_file(encrypted_json, document_path)
