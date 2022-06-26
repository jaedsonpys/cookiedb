import json
import os

from typing import Union
from datetime import datetime
from cryptography.fernet import Fernet


class JSONHandler:
    def __init__(self, enc_key: Union[bytes, str]):
        self._fernet = Fernet(enc_key)

    @staticmethod
    def _save_file(file_content: str, local: str) -> None:
        with open(local, 'w') as writer:
            writer.write(file_content)

    def encrypt_json(self, obj: dict) -> str:
        dict_str = json.dumps(obj)
        encrypted_dict = self._fernet.encrypt(dict_str.encode())
        return encrypted_dict.decode()

    def create_json_database(self, name: str, local: str) -> dict:
        database_path = os.path.join(local, name)
        created_time = str(datetime.now().replace(microsecond=0))

        database = {
            'name': name,
            'created_at': created_time,
            'updated_at': created_time,
            'items': {}
        }

        encrypted_data = self.encrypt_json(database)
        self._save_file(encrypted_data, database_path)

        return database


if __name__ == '__main__':
    handler = JSONHandler(Fernet.generate_key())
    handler.create_json_database('MyDatabase', './')
