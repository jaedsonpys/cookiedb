import hashlib


class Cryptography:
    def __init__(self, key: str) -> None:
        hash_key = hashlib.sha256(key.encode()).digest()
        self._encryption_key = hash_key[:128]
        self._signature_key = hash_key[128:]
