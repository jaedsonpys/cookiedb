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
from io import BufferedWriter
from typing import Union, Any, Tuple, Iterator

from . import exceptions
from ._encrypt import Cryptography
from ._item import Item


class Document:
    def __init__(self, cryptography: Cryptography, document_path: str) -> None:
        self._crypt = cryptography
        self._document_path = document_path

    def _dict_to_path(self, data: dict, basepath: str = None) -> list:
        items = []

        for key, value in data.items():
            if basepath:
                key = '/'.join((str(basepath), str(key)))

            if isinstance(value, dict):
                v_items = self._dict_to_path(value, key)
                items.extend(v_items)
            else:
                items.append((key, value))

        return items

    def _read_doc(self) -> Iterator[bytes]:
        with open(self._document_path, 'rb') as doc:
            while True:
                _line_len = doc.read(2)

                if not _line_len or _line_len == b'\x00':
                    break

                full_len, = struct.unpack('<H', _line_len)
                yield doc.read(full_len)

    @staticmethod
    def create_document(self) -> None:
        with open(self._document_path, 'w') as doc:
            doc.write('')

    def _encrypt(self, data: bytes) -> bytes:
        return self._crypt.encrypt(data)

    def _decrypt(self, encrypted: bytes) -> bytes:
        return self._crypt.decrypt(encrypted)

    def _add_item(self, path: str, value: Any, fp: BufferedWriter) -> None:
        new_item = Item.create(path, value)
        encrypted_item = self._encrypt(new_item)
        fp.write(struct.pack('<H', len(encrypted_item)))
        fp.write(encrypted_item)

    def add(self, path: str, value: Any) -> None:
        with open(self._document_path, 'wb') as doc:
            if isinstance(value, dict):
                new_items = self._dict_to_path(value, path)
                for new_item in new_items:
                    path, value = new_item
                    self._add_item(path, value, doc)
            else:
                self._add_item(path, value, doc)

    def get(self, path: str) -> Union[Tuple[str, Any], None]:
        path = path.encode()

        with open(self._document_path, 'rb') as doc:
            for line in self._read_doc():
                decrypted_item = self._decrypt(line)
                item = Item(decrypted_item)
                item_path = item.get_path()

                if item_path == path:
                    return item_path, item.get_value()
