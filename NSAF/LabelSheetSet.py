import os

from os import path
from csv import DictReader

from . import LABEL_SHEET_ITEMS
from .LabelSheet import LabelSheet

class LabelSheetSet():
    def __init__(self, dir, lang = None):
        main_path = path.join(dir, 'label.csv')
        assert os.access(main_path, os.R_OK), 'Main label file not readable.'

        self.main_sheet = LabelSheet(main_path)
        _available_items = self.main_sheet.available_items
        assert all(map(lambda x: x in _available_items, LABEL_SHEET_ITEMS)), 'Not a standatd label sheet.'

        l10n_path = path.join(dir, 'label.%s.csv' % lang)

        if lang:
            self.l10n_exists = os.access(main_path, os.R_OK)
        else:
            self.l10n_exists = False
        
        if self.l10n_exists:
            self.l10n_sheet = LabelSheet(l10n_path)
        else:
            self.l10n_sheet = None
    
    def query(self, idx):
        if not self.l10n_exists:
            return self.main_sheet.query(idx)
        else:
            return {**self.main_sheet.query(idx), **self.l10n_sheet.query(idx)}
