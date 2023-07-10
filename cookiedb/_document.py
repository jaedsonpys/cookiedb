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
from typing import Union, Any, Tuple

from . import exceptions
from ._encrypt import Cryptography

VALUE_MAP = {
    str: (1, None, lambda vlen: f'{vlen}s'),
    int: (2, 4, 'i'),
    float: (3, 4, 'f'),
}


class Document:
    def __init__(self, cryptography: Cryptography, document_path: str) -> None:
        self._crypt = cryptography
        self._document_path = document_path

    def _encode(path: str, value: Any) -> bytes:
        path_len = len(path)
        value_type, value_len, value_format = VALUE_MAP[type(value)]

        if value_type == 1:
            value = value.encode()
            value_len = len(value)
            value_format = value_format(value_len)

        # <path len> <path> :: <value len> <value type> <value>
        _packv = (path_len, path.encode(), value_len, value_type, value)
        return struct.pack(f'<H{path_len}s HH{value_format}', *_packv)

    def _decode_path(item: bytes) -> Tuple[int, str]:
        item_io = BytesIO(item)
        path_len, = struct.unpack('<H', item_io.read(2))
        path, = struct.unpack(f'<{path_len}s', item_io.read(path_len))
        return path_len, path

    def _decode_value(path_len: int, item: bytes) -> Union[int, float, str]:
        item_io = BytesIO(item)
        path_header_len = path_len + 2
        item_io.seek(path_header_len)

        value_len, value_type = struct.unpack('<HH', item_io.read(4))
        value_buffer = item_io.read(value_len)

        if value_type == 1:
            value, = struct.unpack(f'<{value_len}s', value_buffer)
            value = value.decode()
        elif value_type == 2:
            value, = struct.unpack(f'<i', value_buffer)
        elif value_type == 3:
            value, = struct.unpack(f'<f', value_buffer)

        return value
