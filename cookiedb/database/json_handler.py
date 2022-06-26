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
        self._database_local = database_local

    @staticmethod
    def _save_file(file_content: str, local: str) -> None:
        with open(local, 'w') as writer:
            writer.write(file_content)

    def encrypt_json(self, obj: dict) -> str:
        dict_str = json.dumps(obj)
        encrypted_dict = self._fernet.encrypt(dict_str.encode())
        return encrypted_dict.decode()

    def decrypt_json(self, encrypted: bytes) -> dict:
        decrypted_json = self._fernet.decrypt(encrypted)
        json_data = json.loads(decrypted_json)
        return json_data

    def create_json_database(self, name: str) -> dict:
        database_path = os.path.join(self._database_local, name)
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
    handler = JSONHandler(Fernet.generate_key(), '../databases-test')
    handler.create_json_database('MyDatabase')
