from PyQt5 import QtWidgets


class ProgressBar(QtWidgets.QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEnabled(False)
        self.setProperty("value", 0)
        self.setTextVisible(True)
        self.setObjectName("progressBar")
        self.raw_progress = 0
