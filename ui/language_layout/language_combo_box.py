from PyQt5 import QtWidgets, QtGui


class LanguageComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setItalic(False)
        self.setFont(font)
        self.setEditable(False)
        self.setMaxVisibleItems(10)
        self.setDuplicatesEnabled(False)
        self.setObjectName("languageComboBox")

        self.addItem("Русский")
        self.addItem("Английский")
        self.addItem("Украинский")
        self.addItem("Румынский")

        self.setCurrentIndex(0)
        