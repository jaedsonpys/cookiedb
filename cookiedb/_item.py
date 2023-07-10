import struct
from io import BytesIO
from typing import Any, Union, Tuple

VALUE_MAP = {
    str: (1, None, lambda vlen: f'{vlen}s'),
    int: (2, 4, 'i'),
    float: (3, 4, 'f'),
}


class Item:
    def __init__(self, item: bytes) -> None:
        self._item_io = BytesIO(item)

    @staticmethod
    def create(path: str, value: Any) -> bytes:
        path_len = len(path)
        value_type, value_len, value_format = VALUE_MAP[type(value)]

        if value_type == 1:
            value = value.encode()
            value_len = len(value)
            value_format = value_format(value_len)

        # <path len> <path> :: <value len> <value type> <value>
        _packv = (path_len, path.encode(), value_len, value_type, value)
        return struct.pack(f'<H{path_len}s HH{value_format}', *_packv)

    def get_path(self) -> str:
        path_len, = struct.unpack('<H', self._item_io.read(2))
        path, = struct.unpack(f'<{path_len}s', self._item_io.read(path_len))
        return path

    def get_value(self) -> Union[int, float, str]:
        value_len, value_type = struct.unpack('<HH', self._item_io.read(4))
        value_buffer = self._item_io.read(value_len)

        if value_type == 1:
            value, = struct.unpack(f'<{value_len}s', value_buffer)
            value = value.decode()
        elif value_type == 2:
            value, = struct.unpack(f'<i', value_buffer)
        elif value_type == 3:
            value, = struct.unpack(f'<f', value_buffer)

        return value
