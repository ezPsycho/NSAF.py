import os

from os import path
from csv import DictReader

from . import LABEL_SHEET_ITEMS

__BLANK_QUERY__ = {'idx': 0, 'label': '', 'name': '', 'abbr': ''}

class LabelSheet():
    def __init__(self, x):
        assert os.access(x, os.R_OK), 'Main label file not readable.'

        self.labels = {}
        self.available_items = []

        with open(x, 'r', encoding='utf-8') as f:
            reader = DictReader(f)
            
            for _row in reader:
                _row['idx'] = int(_row['idx'])
                self.labels[_row['idx']] = _row
            
        for _col_name in LABEL_SHEET_ITEMS:
            if _col_name in _row:
                self.available_items.append(_col_name)
        

    def query(self, idx):
        if idx in self.labels:
            return self.labels[idx]
        else:
            return __BLANK_QUERY__

    def available(self, col):
        return col in self.available_items