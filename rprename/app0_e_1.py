# -*- coding: utf-8 -*-
# rprename/app.py

"""
This module provides the RP Renamer application
"""

import sys

from PySide6.QtWidgets import QApplication

from .views1 import Window
# from .views0 import Window

def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
#: