from PyQt5 import QtWidgets, QtGui


class LanguageLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setStyleSheet("font-weight: bold")
        self.setObjectName("languageLabel")
