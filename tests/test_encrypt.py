import sys

import bupytest

sys.path.insert(0, './')

from cookiedb import _encrypt


class TestEncryption(bupytest.UnitTest):
    def __init__(self) -> None:
        self._key = 'secret-key'
        self._fake_key = 'my-fake-secret-key'
        self._enc = _encrypt.Cryptography(self._key)

        self._data = b'My name is John'

    def test_encrypt_data(self):
        encrypted = self._enc.encrypt(self._data)
        self.assert_true(encrypted != self._data)


if __name__ == '__main__':
    bupytest.this()
