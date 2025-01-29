# -*- coding: utf-8 -*-
# rprename/rename.py

"""
This module provides the Renamer and ThreadedRenamer classes to rename 
multiple files.
"""

import time
from pathlib import Path
from typing import Any, Callable, Iterable

from PySide6.QtCore import QObject, Signal, QThread

from .utils import ensure_iterable


type QtSlot = Callable[..., Any]
type QtSlots = QtSlot | Iterable[QtSlot]


class Renamer(QObject):
    # Define custom signals
    progressed = Signal(int)
    renamedFile = Signal(Path)
    finished = Signal()

    def __init__(
            self, 
            files: Iterable[Path], 
            prefix: str,
            deleteLaterOnFinished = True,
            onProgressed: QtSlots = tuple(),
            onRenamedFile: QtSlots = tuple(),
            onFinished: QtSlots = tuple(),
    ):
        super().__init__()
        self._files = files
        self._prefix = prefix

        for slot in ensure_iterable(onProgressed):
            self.progressed.connect(slot)
        for slot in ensure_iterable(onRenamedFile):
            self.renamedFile.connect(slot)
        for slot in ensure_iterable(onFinished):
            self.finished.connect(slot)

        if deleteLaterOnFinished:
            self.finished.connect(self.deleteLater)
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

class ThreadedRenamer(Renamer):
    def __init__(self, *args, start = False, **kargs):
        super().__init__(*args, **kargs)
        self._thread = QThread()
        self._thread.started.connect(self.rename_files)
        self._thread.finished.connect(self._thread.deleteLater)
        self.moveToThread(self._thread)
        self.finished.connect(self._thread.quit)
        if start:
            self._thread.start()
    #:

    def start(self):
        self._thread.start()
    #:
#:

# ThreadedRenamer(['alb', 'dasda'], 23, prefix = 'XPTO')

# args = (['alb', 'dasda'], 23)
# kargs = {'prefix': 'XPTO'}
