from PyQt5 import QtWidgets

import ui


class CommentLayout(QtWidgets.QVBoxLayout):
    def __init__(self, verticalLayoutWidget, parent=None):
        super().__init__(parent)
        self.setObjectName("commentLayout")

        self.commentLabel = ui.CommentLabel(verticalLayoutWidget)
        self.commentTextEdit = ui.CommentTextEdit(verticalLayoutWidget)

        self.addWidget(self.commentLabel)
        self.addWidget(self.commentTextEdit)

