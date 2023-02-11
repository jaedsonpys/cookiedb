import hashlib
import secrets

from Crypto.Cipher import AES
from Crypto.Util import Padding
from Crypto.Hash import HMAC, SHA256

from . import exceptions


class Cryptography:
    def __init__(self, key: str) -> None:
        """initialize a Cryptography instance.

        :param key: Key to encrypt and decrypt
        :type key: str
        """

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
        """Encrypt a data in bytes.

        The result will be a string in bytes containing
        the length of the encrypted data, initialization
        vector (IV), encrypted data and a MAC hash.

        :param data: Any data in bytes
        :type data: bytes
        :return: Encrypted data
        :rtype: bytes
        """

        random_iv = secrets.token_bytes(16)
        padding_data = Padding.pad(data, AES.block_size)

        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv=random_iv)
        encrypted_data = cipher.encrypt(padding_data)

        result = (
            len(data).to_bytes(4, 'big')
            + random_iv
            + encrypted_data
        )

        hmac = self._get_hmac(result)
        return (result + hmac)

    def decrypt(self, token: bytes) -> bytes:
        """Decrypt a token in bytes.

        :param token: Encrypted token
        :type token: bytes
        :raises Exception: If token is invalid
        :raises Exception: If token has a invalid signature
        :return: Decrypted data
        :rtype: bytes
        """

        random_iv = token[4:20]
        mac = token[-32:]
        encrypted_data = token[20:-32]

        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv=random_iv)
        
        if self._valid_hmac(mac, token[:-32]):
            try:
                decrypted_data = cipher.decrypt(encrypted_data)
                unpad_data = Padding.unpad(decrypted_data, AES.block_size)
            except ValueError:
                raise exceptions.InvalidTokenError('The token is invalid') from None
            return unpad_data
        else:
            raise exceptions.InvalidSignatureError('Token signature don\'t match')

    def get_token_size(self, token: bytes) -> int:
        """Return the encrypted token size.

        :param token: Encrypted token
        :type token: bytes
        :return: Data size in bytes
        :rtype: int
        """

        size = int.from_bytes(token[:4], 'big')
        return size
