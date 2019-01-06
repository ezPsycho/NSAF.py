import os
import struct

from . import DTYPE_FORMATS, DTYPE_MARKS

def newNsaf(x, path, dtype = 'uint16', offset = (0,0,0)):
    assert dtype in DTYPE_MARKS, '`dtype` should be one of `uint16`, `uint32`, `float32`, `float64`.'
    assert len(x.shape) == 3, '`x` must be a 3d array.'
    assert os.access(os.path.dirname(path), os.W_OK), 'The path is not writable.'
    
    dtype_mark = DTYPE_MARKS[dtype]
    dtype_format = DTYPE_FORMATS[dtype]

    with open(path, 'wb') as f:
        f.write(struct.pack('>H', dtype_mark))
        
        for _dim in x.shape:
            f.write(struct.pack('>H', _dim))
        
        for _dim in offset:
            f.write(struct.pack('>H', _dim))
        
        for _ in range(3):
            f.write(struct.pack('>H', 0))
    
        list(map(
            lambda x: f.write(struct.pack(dtype_format, x)), 
            x.flatten()
        ))    
