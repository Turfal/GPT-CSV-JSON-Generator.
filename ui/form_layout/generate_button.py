from PyQt5 import QtWidgets, QtGui


class GenerateButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setItalic(False)
        self.setFont(font)
        self.setObjectName("generateButton")
