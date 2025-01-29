# -*- coding: utf-8 -*-
# rprename/views.py

"""
This module provides the RP Renamer main window.
"""

from collections import deque
from pathlib import Path

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QFileDialog, QWidget

from .ui.window import Ui_Window
from .rename1 import ThreadedRenamer

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ADDED: added the following lines to avoid having to compile the 'ui'
# file manually each time we change it in the designer.

from .utils import compile_ui_if_needed_or_exit

UI_FILE_PATH = f'rprename/ui/window.ui'
UI_CLASS_FILE_PATH = f'rprename/ui/window.py'

compile_ui_if_needed_or_exit(UI_FILE_PATH, UI_CLASS_FILE_PATH)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


FILTERS = ';;'.join(
    (
        'JPG Files (*.jpg)',
        'JPEG Files (*.jpeg)',
        'PNG Files (*.png)',
        'GIF Files (*.gif)',
        'Text Files (*.txt)',
        'Python Files (*.py)',
    )
)

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self._setupUI()
        self._connect_signals_slots()
        self._update_state_when_no_files()
    #:

    def _setupUI(self):
        self.setupUi(self)
    #:

    def _connect_signals_slots(self):
        self.loadFilesButton.clicked.connect(self.load_files)
        self.renameFilesButton.clicked.connect(self.rename_files)
        self.prefixEdit.textChanged.connect(self._update_state_when_ready)
    #:

    def load_files(self):
        self.dstFileList.clear()
        init_dir = self.dirEdit.text() if self.dirEdit.text() else str(Path.home) 
        files, filter_ = QFileDialog.getOpenFileNames(
            self, "Choose Files to Rename", init_dir, filter=FILTERS
        )

        if len(files) > 0:
            file_extension = filter_[filter_.index('*') : -1]
            self.extensionLabel.setText(file_extension)
            src_dir_name = str(Path(files[0]).parent)
            self.dirEdit.setText(src_dir_name)
            for file in files:
                file_path = Path(file)
                if file_path not in self._files:   # let's avoid file duplication...
                    self._files.append(file_path)
                    self.srcFileList.addItem(file)
            self._initial_file_count = len(self._files)
            self._update_state_when_files_loaded()
    #:

    def rename_files(self):
        self._start_renamer()
        self._update_state_while_renaming()
    #:

    def _start_renamer(self):
        prefix = self.prefixEdit.text()
        self._renamer = ThreadedRenamer(
            files = tuple(self._files),
            prefix = prefix,
            onProgressed = self._update_progress_bar,
            onRenamedFile = self._update_state_when_file_renamed,
            onFinished = self._update_state_when_no_files,
            start = True,
        )
    #:

    def _update_state_when_no_files(self):
        self._files: deque[Path] = deque()
        self._initial_file_count = 0     # len(self._files)
        self.loadFilesButton.setEnabled(True)
        self.loadFilesButton.setFocus()
        self.renameFilesButton.setEnabled(False)
        self.prefixEdit.clear()
        self.prefixEdit.setEnabled(False)
    #:

    def _update_state_when_files_loaded(self):
        self.prefixEdit.setEnabled(True)
        self.prefixEdit.setFocus()
        self.progressBar.setValue(0)
    #:

    def _update_state_when_ready(self):
        self.renameFilesButton.setEnabled(
            len(self.prefixEdit.text().strip()) > 0
        )
    #:

    def _update_state_while_renaming(self):
        self.loadFilesButton.setEnabled(False)
        self.renameFilesButton.setEnabled(False)
        self.prefixEdit.setEnabled(False)
    #:

    def _update_state_when_file_renamed(self, newFile: Path):
        self._files.popleft()
        self.srcFileList.takeItem(0)
        self.dstFileList.addItem(str(newFile))
    #:

    def _update_progress_bar(self, file_number: int):
        progress_percent = int((file_number / self._initial_file_count) * 100)
        self.progressBar.setValue(progress_percent)
    #:
#: