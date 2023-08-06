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
from typing import Any, Union, Iterator, List, Any

from .exceptions import ValueNotSupportedError

VALUE_MAP = {
    str: (1, None, lambda vlen: f'{vlen}s'),
    int: (2, 4, 'i'),
    float: (3, 4, 'f'),
    bool: (4, 1, '?'),
}

INVERSE_VALUE_MAP = {v[0]: (k, v[2]) for k, v in VALUE_MAP.items()}


class Item:
    def __init__(self, item: bytes) -> None:
        self._item_io = BytesIO(item)

    @staticmethod
    def create(path: str, value: Any) -> bytes:
        type_map = VALUE_MAP.get(type(value))
        
        if not type_map:
            raise ValueNotSupportedError(f'Value type {repr(type(value))} not supported')

        path_len = len(path)
        value_type, value_len, value_format = type_map

        if value_type == 1:
            value = value.encode()
            value_len = len(value)
            value_format = value_format(value_len)

        # <path len> <path> :: <value len> <value type> <value>
        _packv = (path_len, path.encode(), value_len, value_type, value)
        return struct.pack(f'<H{path_len}s HH{value_format}', *_packv)

    @classmethod
    def create_list(cls, path: str, value: list) -> Iterator[List[bytes]]:
        if not path.startswith('#'):
            yield cls.create(f'@list:{path}', len(value))
        else:
            path = path.strip('#')

        for i, v in enumerate(value):
            list_element_path = f'#{path}/{i}'

            if isinstance(v, dict):
                items = cls._dict_to_items(v, list_element_path)
                for item in items:
                    yield item
            elif isinstance(v, list):
                items = cls.create_list(list_element_path, v)
                for item in items:
                    yield item
            else:
                yield cls.create(list_element_path, v)

    @classmethod
    def _dict_to_items(cls, _dict: dict, basepath: str = None) -> List[bytes]:
        items = []

        for key, value in _dict.items():
            if basepath:
                key = '/'.join((str(basepath), str(key)))

            if isinstance(value, dict):
                v_items = cls._dict_to_items(value, key)
                items.extend(v_items)
            elif isinstance(value, list):
                items.extend(cls.create_list(key, value))
            else:
                items.append(cls.create(key, value))

        return items

    def get_path(self) -> bytes:
        path_len, = struct.unpack('<H', self._item_io.read(2))
        path, = struct.unpack(f'<{path_len}s', self._item_io.read(path_len))
        return path

    def get_value(self) -> Union[int, float, str]:
        value_len, value_type_n = struct.unpack('<HH', self._item_io.read(4))
        value_buffer = self._item_io.read(value_len)
        value_type, value_format = INVERSE_VALUE_MAP[value_type_n]

        if value_type == str:
            value, = struct.unpack(f'<{value_format(value_len)}', value_buffer)
            value = value.decode()
        else:
            value, = struct.unpack(f'<{value_format}', value_buffer)

        return value
