import hashlib
import secrets

from Crypto.Cipher import AES
from Crypto.Util import Padding
from Crypto.Hash import HMAC, SHA256


class Cryptography:
    def __init__(self, key: str) -> None:
        hash_key = hashlib.sha256(key.encode()).digest()
        self._encryption_key = hash_key[:128]
        self._signature_key = hash_key[128:]

    def _get_hmac(self, data: bytes) -> bytes:
        hmac = HMAC.new(self._signature_key, digestmod=SHA256)
        hmac.update(data)
        return hmac.digest()

    def _valid_hmac(self, mac: bytes, data: bytes) -> bool:
        hmac = HMAC.new(self._signature_key, digestmod=SHA256)
        hmac.update(data)

        try:
            hmac.verify(mac)
        except ValueError:
            return False
        else:
            return True
    
    def encrypt(self, data: bytes) -> bytes:
        random_iv = secrets.token_bytes(16)
        padding_data = Padding.pad(data, AES.block_size)

        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv=random_iv)
        encrypted_data = cipher.encrypt(padding_data)
        hmac = self._get_hmac(encrypted_data)

        encrypted_data_len = len(encrypted_data).to_bytes(4, 'big')

        result = (
            encrypted_data_len
            + random_iv
            + hmac
            + encrypted_data
        )

        return result
