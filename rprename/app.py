# -*- coding: utf-8 -*-
# rprename/app.py

"""
This module provides the RP Renamer application
"""

import sys
import asyncio

# from PySide6.QtWidgets import QApplication

import qasync

from .views import Window

# def main():
#     app = QApplication(sys.argv)
#     win = Window()
#     win.show()
#     sys.exit(app.exec())
# #:

def main():
    qasync.QApplication(sys.argv)
    with qasync.QEventLoop() as event_loop:
        asyncio.set_event_loop(event_loop)
        win = Window()
        win.show()
        event_loop.run_forever()
#: