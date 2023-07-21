from PyQt5 import QtWidgets, QtGui


class TitleCheckBox(QtWidgets.QCheckBox):
    def __init__(self, parent):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.setFont(font)
        self.setObjectName("titleCheckBox")


