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
        with open(local, 'r') as writer:
            writer.write(file_content)

    def encrypt_json(self, obj: dict) -> str:
        dict_str = json.dumps(obj)
        encrypted_dict = self._fernet.encrypt(dict_str.encode())
        return encrypted_dict.decode()
