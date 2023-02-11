# Copyright 2023 Jaedson Silva

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

import os
import pickle
from datetime import datetime
from typing import Union

from . import exceptions
from ._encrypt import Cryptography


class Document:
    def __init__(self, key: bytes, database_local: str) -> None:
        self._crypt = Cryptography(key)
        self._document_local = database_local

    @staticmethod
    def _save_file(file_content: str, filepath: str) -> None:
        with open(filepath, 'wb') as writer:
            writer.write(file_content)

    def exists_document(self, database: str) -> bool:
        document_path = os.path.join(self._document_local, database + '.cookiedb')
        return os.path.isfile(document_path)

    def _encrypt(self, obj: dict) -> str:
        pickle_file = pickle.dumps(obj)
        encrypted_data = self._crypt.encrypt(pickle_file)
        return encrypted_data

    def _decrypt(self, encrypted: bytes) -> dict:
        decrypted_data = self._fernet.decrypt(encrypted)
        data = pickle.loads(decrypted_data)
        return data

    def create_document(self, name: str) -> dict:
        document_path = os.path.join(self._document_local, name + '.cookiedb')
        created_time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')

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
