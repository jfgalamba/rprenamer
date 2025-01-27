# -*- coding: utf-8 -*-
# rprename/views.py

"""
This module provides the RP Renamer main window.
"""

from collections import deque
from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog, QWidget, QMessageBox

from .ui.window import Ui_Window

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ADDED: added the following lines to avoid having to compile the 'ui'
# file manually each time we change it in the designer.

from .utils import compile_ui_if_needed_or_exit
from .utils import show_info

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
    #:

    def _update_state_when_no_files(self):
        self._files = deque()
        self._files_count = 0
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
                if file_path not in self._files:   # let's avoid duplicate files
                    self._files.append(file_path)
                    self.srcFileList.addItem(file)
            self._files_count = len(self._files)

            # self._update_state_when_files_loaded()
    #:

    def rename_files(self):
        self._run_renamer_thread()

    #:

    def _run_renamer_thread(self):
        
    #:
#: