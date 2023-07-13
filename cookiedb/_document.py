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

import os
import struct
from io import BufferedWriter
from typing import Union, Any, Tuple, Iterator, List

from . import exceptions
from ._encrypt import Cryptography
from ._item import Item


class Document:
    def __init__(self, cryptography: Cryptography, document_path: str) -> None:
        self._crypt = cryptography
        self._document_path = document_path

        if not os.path.isfile(document_path):
            self.create_document()
        else:
            first_item = next(self._read_doc())
            
            try:
                self._crypt.decrypt(first_item)
            except exceptions.InvalidTokenError:
                raise exceptions.InvalidKeyError('Invalid database key') from None

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

    @staticmethod
    def _to_dict_tree(items: List[Tuple[str, Any]]) -> dict:
        result = {}

        for sp, vl in items:
            p_result = result
            sp_split = [x for x in sp.split('/') if x]
            max_i = len(sp_split) - 1

            for i, p in enumerate(sp_split):
                if max_i == i:
                    p_result[p] = vl
                else:
                    p_result = p_result.setdefault(p, {})

        return result

    def _read_doc(self) -> Iterator[bytes]:
        with open(self._document_path, 'rb') as doc:
            while True:
                _line_len = doc.read(2)

                if not _line_len or _line_len == b'\x00':
                    break

                full_len, = struct.unpack('<H', _line_len)
                yield doc.read(full_len)

    def create_document(self) -> None:
        with open(self._document_path, 'wb') as doc:
            self._add_item('@checkEncrypt', True, doc)

    def _add_item(self, path: str, value: Any, fp: BufferedWriter) -> None:
        new_item = Item.create(path, value)
        encrypted_item = self._crypt.encrypt(new_item)
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

    def get(self, path: str) -> Union[Any, None]:
        path = path.encode()
        items = []

        for line in self._read_doc():
            decrypted_item = self._crypt.decrypt(line)
            item = Item(decrypted_item)
            item_path = item.get_path()

            if item_path == path:
                return item.get_value()
            elif item_path.startswith(path):
                sub_path = item_path.replace(path, b'')
                items.append((sub_path.decode(), item.get_value()))

        if items:
            result = self._to_dict_tree(items)
            return result
