import os
import struct

from . import DTYPE_FORMATS, DTYPE_MARKS, DTYPE_LENGTHS

class Nsaf():
    def __init__(self, path):
        assert os.access(path, os.R_OK), 'the file is not readable.'

        self._file = open(path, 'rb')
        self._dtype_mark = self.get_meta_bytes(0)
        
        for _dtype, _mark in DTYPE_MARKS.items():
            if _mark == self._dtype_mark:
                self.dtype = _dtype
                break
        
        self._unit_len = DTYPE_LENGTHS[self.dtype]
        self._dtype_format = DTYPE_FORMATS[self.dtype]

        self._d0 = self.get_meta_bytes(1)
        self._d1 = self.get_meta_bytes(2)
        self._d2 = self.get_meta_bytes(3)
        self.shape = (self._d0, self._d1, self._d2)

        self._o0 = self.get_meta_bytes(4)
        self._o1 = self.get_meta_bytes(5)
        self._o2 = self.get_meta_bytes(6)
        self.offset = (self._o0, self._o1, self._o2)
    
    def get_bytes(self, position, length):
        self._file.seek(position, 0)
        return self._file.read(length)

    def get_meta_bytes(self, position):
        bytes = self.get_bytes(position * 2, 2)
        return struct.unpack('>H', bytes)[0]
    
    def get_data_bytes(self, idx):
        assert len(idx) == 3 or not all(isinstance(x, int) for x in idx), 'Idx should include three ints.'

        byte_pos = (idx[0] * self._d1 * self._d2 + idx[1] * self._d2 + idx[2]) * self._unit_len
        bytes = self.get_bytes(10 * 2 + byte_pos, self._unit_len)

        return struct.unpack(self._dtype_format, bytes)[0]

    def query(self, coord):
        return self.get_data_bytes(self.w2d(coord))
    
    def w2d(self, coord):
        return (
            coord[0] + self._o0, 
            coord[1] + self._o1, 
            coord[2] + self._o2
        )

    def d2w(self, coord):
        return (
            coord[0] - self._o0, 
            coord[1] - self._o1, 
            coord[2] - self._o2
        )

    def close(self):
        self._file.close()