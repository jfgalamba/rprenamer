# -*- coding: utf-8 -*-
# rprename/views.py

"""
This module provides the RP Renamer main window.
"""

from collections import deque
from pathlib import Path

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFileDialog, QWidget

from .ui.window import Ui_Window

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ADDED: added the following lines to avoid having to compile the 'ui'
# file manually each time we change it in the designer.

from .utils import compile_ui_if_needed_or_exit

UI_FILE_PATH = f'rprename/ui/window.ui'
UI_CLASS_FILE_PATH = f'rprename/ui/window.py'

compile_ui_if_needed_or_exit(UI_FILE_PATH, UI_CLASS_FILE_PATH)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self._setupUI()
    #:

    def _setupUI(self):
        self.setupUi(self)
    #:
#: