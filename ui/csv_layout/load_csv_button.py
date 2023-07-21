from PyQt5.QtWidgets import QPushButton
from PyQt5 import QtGui


class LoadCSVButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent=parent)

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setItalic(False)
        self.setFont(font)
        self.setObjectName("loadCSVButton")

