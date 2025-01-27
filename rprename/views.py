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

class Window(QWidget, Ui_Window):
    def __init__(self):
        super().__init__()
        self._setupUI()
    #:

    def _setupUI(self):
        self.setupUi(self)
    #:
#: