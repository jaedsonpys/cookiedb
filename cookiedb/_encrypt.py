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

import struct
from io import BytesIO
from hashlib import sha256
from secrets import token_bytes

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

        hash_key = sha256(key.encode()).digest()
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
        the initialization vector (IV), encrypted data
        and a MAC hash.

        :param data: Any data in bytes
        :type data: bytes
        :return: Encrypted data
        :rtype: bytes
        """

        random_iv = token_bytes(16)
        padding_data = Padding.pad(data, AES.block_size)

        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv=random_iv)
        encrypted_data = cipher.encrypt(padding_data)

        enc_data_mac = self._get_hmac(encrypted_data)
        enc_data_len = len(encrypted_data)
        enc_data_mac_len = len(enc_data_mac)

        pack_values = (enc_data_len, enc_data_mac_len,
                       random_iv, encrypted_data, enc_data_mac)
        result = struct.pack(f'<HH 16s {enc_data_len}s {enc_data_mac_len}s', *pack_values)

        return result

    def decrypt(self, token: bytes) -> bytes:
        """Decrypt a token in bytes.

        :param token: Encrypted token
        :type token: bytes
        :raises InvalidTokenError: If token is invalid
        :raises InvalidSignatureError: If token has a invalid signature
        :return: Decrypted data
        :rtype: bytes
        """

        token_buf = BytesIO(token)
        enc_len, mac_len = struct.unpack('<HH', token_buf.read(4))
        flen = (enc_len + mac_len) + 16
        iv, encrypted_data, mac = struct.unpack(f'<16s {enc_len}s {mac_len}s', token_buf.read(flen))

        cipher = AES.new(self._encryption_key, AES.MODE_CBC, iv=iv)
        
        if self._valid_hmac(mac, encrypted_data):
            try:
                decrypted_data = cipher.decrypt(encrypted_data)
                unpad_data = Padding.unpad(decrypted_data, AES.block_size)
            except ValueError:
                raise exceptions.InvalidTokenError('The token is invalid') from None
            return unpad_data
        else:
            raise exceptions.InvalidSignatureError('Token signature don\'t match')
