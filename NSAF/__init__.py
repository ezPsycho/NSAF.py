DTYPE_FORMATS = {
    'uint16': '>H',
    'uint32': '>I',
    'float32': '>f',
    'float64': '>d'
}

DTYPE_MARKS = {
    'uint16': 1,
    'uint32': 2,
    'float32': 11,
    'float64': 21
}

DTYPE_LENGTHS = {
    'uint16': 2,
    'uint32': 2,
    'float32': 4,
    'float64': 8
}

LABEL_SHEET_ITEMS = ['label', 'name', 'abbr']