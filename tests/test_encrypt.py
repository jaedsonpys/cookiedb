import sys

import bupytest

sys.path.insert(0, './')

from cookiedb import _encrypt


class TestEncryption(bupytest.UnitTest):
    def __init__(self) -> None:
        self._key = 'secret-key'
        self._fake_key = 'my-fake-secret-key'
        self._enc = _encrypt.Cryptography(self._key)


if __name__ == '__main__':
    bupytest.this()
