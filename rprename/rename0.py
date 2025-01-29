# -*- coding: utf-8 -*-
# rprename/rename0.py

"""
This module provides the Renamer class to rename multiple files.
"""

import time
from pathlib import Path
from typing import Iterable

from PySide6.QtCore import QObject, Signal

class Renamer(QObject):
    # Define custom signals
    progressed = Signal(int)
    renamedFile = Signal(Path)
    finished = Signal()

    def __init__(self, files: Iterable[Path], prefix: str):
        super().__init__()
        self._files = files
        self._prefix = prefix
    #:

    def rename_files(self):
        for file_number, file in enumerate(self._files, 1):
            new_file = file.parent.joinpath(
                f'{self._prefix}{file_number}{file.suffix}'
            )
            file.rename(new_file)
            time.sleep(1.1)   # Let's slow down a bit (comment this for the process to go faster)
            self.progressed.emit(file_number)
            self.renamedFile.emit(new_file)
        self.finished.emit()
    #:
#:
