# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'window.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QProgressBar, QPushButton,
    QSizePolicy, QSplitter, QVBoxLayout, QWidget)

class Ui_Window(object):
    def setupUi(self, Window):
        if not Window.objectName():
            Window.setObjectName(u"Window")
        Window.resize(752, 522)
        self.gridLayout = QGridLayout(Window)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(Window)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 20))
        self.label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)

        self.dirEdit = QLineEdit(Window)
        self.dirEdit.setObjectName(u"dirEdit")
        self.dirEdit.setMinimumSize(QSize(0, 30))
        self.dirEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.dirEdit, 1, 0, 1, 2)

        self.loadFilesButton = QPushButton(Window)
        self.loadFilesButton.setObjectName(u"loadFilesButton")
        self.loadFilesButton.setMinimumSize(QSize(0, 35))
        self.loadFilesButton.setMaximumSize(QSize(16777215, 35))

        self.gridLayout.addWidget(self.loadFilesButton, 1, 2, 1, 1)

        self.splitter = QSplitter(Window)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        font = QFont()
        font.setBold(True)
        self.label_2.setFont(font)

        self.verticalLayout.addWidget(self.label_2)

        self.srcFileList = QListWidget(self.layoutWidget)
        self.srcFileList.setObjectName(u"srcFileList")

        self.verticalLayout.addWidget(self.srcFileList)

        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.layoutWidget1)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)

        self.verticalLayout_2.addWidget(self.label_3)

        self.dstFileList = QListWidget(self.layoutWidget1)
        self.dstFileList.setObjectName(u"dstFileList")

        self.verticalLayout_2.addWidget(self.dstFileList)

        self.splitter.addWidget(self.layoutWidget1)

        self.gridLayout.addWidget(self.splitter, 2, 0, 1, 3)

        self.label_4 = QLabel(Window)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 20))
        self.label_4.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 3)

        self.prefixEdit = QLineEdit(Window)
        self.prefixEdit.setObjectName(u"prefixEdit")
        self.prefixEdit.setMinimumSize(QSize(0, 30))
        self.prefixEdit.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.prefixEdit, 4, 0, 1, 1)

        self.extensionLabel = QLabel(Window)
        self.extensionLabel.setObjectName(u"extensionLabel")
        self.extensionLabel.setMinimumSize(QSize(0, 30))
        self.extensionLabel.setMaximumSize(QSize(16777215, 30))

        self.gridLayout.addWidget(self.extensionLabel, 4, 1, 1, 1)

        self.renameFilesButton = QPushButton(Window)
        self.renameFilesButton.setObjectName(u"renameFilesButton")
        self.renameFilesButton.setMinimumSize(QSize(0, 35))
        self.renameFilesButton.setMaximumSize(QSize(16777215, 35))

        self.gridLayout.addWidget(self.renameFilesButton, 4, 2, 1, 1)

        self.progressBar = QProgressBar(Window)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.gridLayout.addWidget(self.progressBar, 5, 0, 1, 3)


        self.retranslateUi(Window)

        QMetaObject.connectSlotsByName(Window)
    # setupUi

    def retranslateUi(self, Window):
        Window.setWindowTitle(QCoreApplication.translate("Window", u"RP Renamer", None))
        self.label.setText(QCoreApplication.translate("Window", u"Last Source Directory:", None))
        self.loadFilesButton.setText(QCoreApplication.translate("Window", u"Load Files", None))
#if QT_CONFIG(shortcut)
        self.loadFilesButton.setShortcut(QCoreApplication.translate("Window", u"L", None))
#endif // QT_CONFIG(shortcut)
        self.label_2.setText(QCoreApplication.translate("Window", u"Files To Rename", None))
        self.label_3.setText(QCoreApplication.translate("Window", u"Renamed Files", None))
        self.label_4.setText(QCoreApplication.translate("Window", u"Filename Prefix:", None))
        self.prefixEdit.setText("")
        self.prefixEdit.setPlaceholderText(QCoreApplication.translate("Window", u"Rename your files to...", None))
        self.extensionLabel.setText(QCoreApplication.translate("Window", u"*.jpg", None))
        self.renameFilesButton.setText(QCoreApplication.translate("Window", u"&Rename", None))
    # retranslateUi

