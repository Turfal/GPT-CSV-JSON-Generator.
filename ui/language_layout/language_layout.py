from PyQt5 import QtWidgets

import ui


class LanguageLayout(QtWidgets.QVBoxLayout):
    def __init__(self, verticalLayoutWidget, parent=None):
        super().__init__(parent)
        self.setObjectName("languageLayout")

        self.languageLabel = ui.LanguageLabel(verticalLayoutWidget)
        self.languageComboBox = ui.LanguageComboBox(verticalLayoutWidget)

        self.addWidget(self.languageLabel)
        self.addWidget(self.languageComboBox)
