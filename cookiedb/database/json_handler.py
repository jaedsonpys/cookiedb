import json
import os

from datetime import datetime
from cryptography.fernet import Fernet


class JSONHandler:
    def __init__(self, enc_key: str):
        self._fernet = Fernet(enc_key)

    def encrypt_json(self, obj: dict) -> str:
        dict_str = json.dumps(obj)
        encrypted_dict = self._fernet.encrypt(dict_str.encode())
        return encrypted_dict.decode()
