import csv

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

import ui


def read_from_csv(filename, delimiter=","):
    data = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)

        for row in reader:
            data.append(row)

    return data


class CSVLayout(QtWidgets.QVBoxLayout):
    def __init__(self, verticalLayoutWidget, parent=None):
        super().__init__(parent)
        self.setSpacing(8)
        self.setObjectName("csvLayout")

        self.loadCSVButton = ui.LoadCSVButton(verticalLayoutWidget)
        self.loadCSVCounterLabel = ui.LoadCSVCounterLabel(verticalLayoutWidget)

        self.addWidget(self.loadCSVButton)
        self.addWidget(self.loadCSVCounterLabel)

        self.open_file_caption = ""
        self.open_file_filter_text = ""

        self.loadCSVButton.clicked.connect(self.event_click)

        self.loadedCSVData = None

    def event_click(self):
        csv_file_name = QFileDialog.getOpenFileName(
            self.loadCSVButton,
            self.open_file_caption,
            filter=self.open_file_filter_text
        )[0]

        csv_data = read_from_csv(csv_file_name, ';')

        self.loadCSVCounterLabel.setText(f"Загружено товаров: {len(csv_data)}")

        self.loadedCSVData = csv_data

    def set_open_file_texts(self, caption, filter_text):
        self.open_file_caption = caption
        self.open_file_filter_text = filter_text
