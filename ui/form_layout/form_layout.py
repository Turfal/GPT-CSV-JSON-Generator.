from PyQt5 import QtWidgets

import ui


class FormLayout(QtWidgets.QFormLayout):
    def __init__(self, verticalLayoutWidget):
        super().__init__()
        self.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.FieldsStayAtSizeHint)
        self.setRowWrapPolicy(QtWidgets.QFormLayout.RowWrapPolicy.WrapAllRows)
        self.setHorizontalSpacing(0)
        self.setVerticalSpacing(9)
        self.setObjectName("formLayout")

        self.generateButton = ui.GenerateButton(verticalLayoutWidget)

        self.tagCheckBoxLabel = ui.TagCheckboxLabel(verticalLayoutWidget)
        self.h1CheckBox = ui.H1CheckBox(verticalLayoutWidget)
        self.keywordsCheckBox = ui.KeywordsCheckBox(verticalLayoutWidget)
        self.descriptionCheckBox = ui.DescriptionCheckBox(verticalLayoutWidget)
        self.titleCheckBox = ui.TitleCheckBox(verticalLayoutWidget)
        self.fullDescriptionCheckBox = ui.FullDescriptionCheckBox(verticalLayoutWidget)
        self.progressBar = ui.ProgressBar(verticalLayoutWidget)

        self.setFormLayoutWidgets()

        self.checkboxesValues = {
            "fullDescription": False,
            "title": False,
            "description": False,
            "keywords": False,
            "h1": False
        }

        self.fullDescriptionCheckBox.stateChanged.connect(self.checkboxes_state_changed)
        self.titleCheckBox.stateChanged.connect(self.checkboxes_state_changed)
        self.descriptionCheckBox.stateChanged.connect(self.checkboxes_state_changed)
        self.keywordsCheckBox.stateChanged.connect(self.checkboxes_state_changed)
        self.h1CheckBox.stateChanged.connect(self.checkboxes_state_changed)

    def setFormLayoutWidgets(self):
        self.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.tagCheckBoxLabel)
        self.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.fullDescriptionCheckBox)
        self.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.titleCheckBox)
        self.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.descriptionCheckBox)
        self.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.keywordsCheckBox)
        self.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.h1CheckBox)
        self.setWidget(6, QtWidgets.QFormLayout.ItemRole.LabelRole, self.generateButton)
        self.setWidget(7, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.progressBar)

    def checkboxes_state_changed(self):
        self.checkboxesValues["fullDescription"] = self.fullDescriptionCheckBox.isChecked()
        self.checkboxesValues["title"] = self.titleCheckBox.isChecked()
        self.checkboxesValues["description"] = self.descriptionCheckBox.isChecked()
        self.checkboxesValues["keywords"] = self.keywordsCheckBox.isChecked()
        self.checkboxesValues["h1"] = self.h1CheckBox.isChecked()
