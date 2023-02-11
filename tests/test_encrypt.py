import sys

import bupytest

sys.path.insert(0, './')

import cookiedb
from cookiedb import _encrypt


class TestEncryption(bupytest.UnitTest):
    def __init__(self) -> None:
        self._enc = _encrypt.Cryptography('secret-key')
        self._fake_enc = _encrypt.Cryptography('fake-secret-key')

        self._data = b'My name is John'

    def test_encrypt_data(self):
        self.encrypted = self._enc.encrypt(self._data)
        self.assert_true(self.encrypted != self._data)

    def test_decrypt_data(self):
        decrypted = self._enc.decrypt(self.encrypted)
        self.assert_expected(decrypted, self._data)

    def test_decrypt_with_invalid_key(self):
        try:
            self._fake_enc.decrypt(self.encrypted)
        except cookiedb.exceptions.InvalidTokenError:
            self.assert_true(True)
        else:
            self.assert_true(False, message='Expected a InvalidTokenError exception')

    def test_get_data_size(self):
        data_size = self._enc.get_token_size(self.encrypted)
        self.assert_expected(data_size, len(self._data))


if __name__ == '__main__':
    bupytest.this()
