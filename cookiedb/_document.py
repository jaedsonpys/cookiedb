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
            with open(self._document_path, 'wb') as doc:
                self._add_item('@checkEncrypt', True, doc)
        else:
            first_item = next(self._read_doc())[1]

            try:
                self._crypt.decrypt(first_item)
            except exceptions.InvalidTokenError:
                raise exceptions.InvalidDatabaseKeyError('Invalid database key') from None

    @staticmethod
    def _to_dict_tree(items: List[Tuple[str, Any]], _list: bool = False) -> dict:
        result = [] if _list else {}

        for path, value in items:
            result_ref = result
            parts = path.strip('/').split('/')
            max_index = len(parts) - 1
            last_index = None

            for i, part in enumerate(parts):
                if i == max_index:
                    if isinstance(result_ref, list) and part.isdigit():
                        result_ref.append(value)
                    elif isinstance(result_ref, list):
                        result_ref[last_index][part] = value
                    else:
                        result_ref[part] = value
                elif part.isdigit():
                    last_index = int(part)
                    try:
                        result_ref = result_ref[last_index]
                    except IndexError:
                        if parts[i + 1].isdigit():
                            dtype = []
                        else:
                            dtype = {}

                        result_ref.insert(last_index, dtype)
                        result_ref = result_ref[last_index]
                elif parts[i + 1].isdigit():
                    result_ref = result_ref.setdefault(part, [])
                else:
                    result_ref = result_ref.setdefault(part, {})

        return result

    def _read_doc(self) -> Iterator[Tuple[bytes]]:
        with open(self._document_path, 'rb') as doc:
            while True:
                _line_len = doc.read(2)

                if not _line_len or _line_len == b'\x00':
                    break

                full_len, = struct.unpack('<H', _line_len)
                yield _line_len, doc.read(full_len)

    def _read_items(self) -> Iterator[Item]:
        for __, line in self._read_doc():
            decrypted_line = self._crypt.decrypt(line)
            yield Item(decrypted_line)

    def _write_item(self, item: bytes, fp: BufferedWriter) -> None:
        encrypted_item = self._crypt.encrypt(item)
        fp.write(struct.pack('<H', len(encrypted_item)))
        fp.write(encrypted_item)

    def _add_item(self, path: str, value: Any, fp: BufferedWriter) -> None:
        new_item = Item.create(path, value)
        self._write_item(new_item, fp)

    def _exists(self, path: str) -> bool:
        path = path.encode()

        for item in self._read_items():
            item_path = item.get_path()

            if item_path == path or item_path.startswith(path):
                return True
            elif item_path.startswith(b''.join((b'@list:', path))):
                return True
            elif item_path.startswith(b''.join((b'#', path))):
                return True

        return False

    def _get_list(self, path: str, _len: int) -> list:
        required_items = [f'#{path}/{i}'.encode() for i in range(_len)]
        list_items = []

        def _in_required(ipath: bytes) -> bool:
            for req_item in required_items:
                if ipath == req_item or ipath.startswith(req_item):
                    return True

            return False

        _encoded_path = path.encode()
        _enc_path_elem = b''.join((b'#', _encoded_path))
        _get_basepath = lambda p: p.replace(_enc_path_elem, b'')

        for item in self._read_items():
            item_path = item.get_path()

            if _in_required(item_path):
                value = item.get_value()
                basepath = _get_basepath(item_path).decode()

                if not item_path.decode()[-1].isdigit():
                    list_items.append((basepath, value))
                else:
                    list_items.append((basepath, value))

        tree_items = self._to_dict_tree(list_items, _list=True)
        return tree_items

    def add(self, path: str, value: Any) -> None:
        if self._exists(path):
            self.update(path, value)
        else:
            with open(self._document_path, 'ab') as doc:
                if isinstance(value, dict):
                    items = Item._dict_to_items(value, path)
                    for item in items:
                        self._write_item(item, doc)
                elif isinstance(value, list):
                    items = Item.create_list(path, value)
                    for item in items:
                        self._write_item(item, doc)
                else:
                    self._add_item(path, value, doc)

    def get(self, path: str) -> Union[Any, None]:
        path = path.encode()
        items = []

        for item in self._read_items():
            item_path = item.get_path()

            if item_path == path:
                return item.get_value()
            elif item_path.startswith(b''.join((b'@list:', path))):
                path_without_prefix = item_path[6:]
                sub_path = path_without_prefix.replace(path, b'')
                item_value = self._get_list(path_without_prefix.decode(), item.get_value())

                if item_path == b''.join((b'@list:', path)):
                    return item_value

                items.append((sub_path.decode(), item_value))
            elif item_path.startswith(path):
                sub_path = item_path.replace(path, b'')
                items.append((sub_path.decode(), item.get_value()))

        if items:
            result = self._to_dict_tree(items)
            return result
        
    def delete(self, path: str) -> None:
        path = path.encode()

        with open(self._document_path + '.temp', 'wb') as _temp_doc:
            for line_len, line in self._read_doc():
                decrypted_item = self._crypt.decrypt(line)
                item = Item(decrypted_item)
                item_path = item.get_path()

                if item_path != path and not item_path.startswith(path):
                    lpath = b''.join((b'@list:', path))
                    lepath = b''.join((b'#', path))

                    if not item_path.startswith(lpath) and not item_path.startswith(lepath):
                        _temp_doc.write(line_len)
                        _temp_doc.write(line)

        os.remove(self._document_path)
        os.rename(self._document_path + '.temp', self._document_path)

    def update(self, path: str, value: Any) -> None:
        self.delete(path)
        self.add(path, value)
