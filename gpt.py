from concurrent.futures import as_completed

import openai
import concurrent.futures
import csv
import json
import re

from PyQt5 import QtWidgets, QtCore

import ui

openai.api_key = "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"


def write_to_csv(filename, headers, data):
    with open(filename, 'w', newline='', encoding="utf-8-sig") as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers, delimiter=";")
        csv_writer.writeheader()
        csv_writer.writerows(data)

    print(f"Write successful: {len(data)} rows")



def create_gpt_completion(message):
    try:
        model_engine = "text-davinci-003"
        max_tokens = 2500

        result = openai.Completion.create(
            model=model_engine,
            prompt=message,
            max_tokens=max_tokens,
            temperature=0.8
        )

        return result.choices[0].text
    except ValueError:
        return f"""{{"text": "","h1": "","title": "","description": "","keywords": ""}}"""


class GPTWorker(QtCore.QThread):
    finished = QtCore.pyqtSignal(list)
    progress = QtCore.pyqtSignal()

    def __init__(self, prompts):
        super().__init__()
        self.prompts = prompts

    def run(self):
        results = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.run_gpt_request, prompt) for prompt in self.prompts]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())

        self.finished.emit(results)

    def run_gpt_request(self, prompt):
        res = create_gpt_completion(prompt)
        self.progress.emit()
        return res


class MainLayout(QtWidgets.QVBoxLayout):
    def __init__(self, verticalLayoutWidget):
        super().__init__(verticalLayoutWidget)
        self.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.setContentsMargins(20, 20, 20, 20)
        self.setSpacing(20)
        self.setObjectName("mainLayout")

        self.csvLayout = ui.CSVLayout(verticalLayoutWidget)
        self.languageLayout = ui.LanguageLayout(verticalLayoutWidget)
        self.commentLayout = ui.CommentLayout(verticalLayoutWidget)
        self.formLayout = ui.FormLayout(verticalLayoutWidget)

        self.addLayouts()
        self.addEventsToButtons()

        self.thread = None
        self.worker = None

    def addLayouts(self):
        self.addLayout(self.csvLayout)
        self.addLayout(self.languageLayout)
        self.addLayout(self.commentLayout)
        self.addLayout(self.formLayout)

    def addEventsToButtons(self):
        self.formLayout.generateButton.clicked.connect(self.send_requests)

    def get_prompt_for_line(self, line):
        if line["_DESCRIPTION_"] != "":
            help_text = line["_DESCRIPTION_"]
        else:
            help_text = line["_NAME_"]

        language = str(self.languageLayout.languageComboBox.currentText())

        help_text += f". {self.commentLayout.commentTextEdit.toPlainText()}"

        # Prompt, который будет отправлен chatgpt
        prompt = \
            f"""
        Сгенерируй JSON-ответ на основе следующего текста:

        {help_text}

        Формат JSON-ответа - JSON следующего вида, где "text" - описание товара, рерайт переданного 
        текста ( оптимальный объем текста 400-800 символов), "h1" - текст для html тэга H1,  
        "title" - текст для html мета-тэга title, "description" - текст для html мета-тэга description (
        рекомендуемая длина 160-170 символов), "keywords" - текст для html мета-тэга keywords (
        разделитель - запятая): 
        {{ 
        "text": "",
        "h1": "",
        "title": "",
        "description": "",
        "keywords": "",
        }}

        Язык всего генерируемого текста: {language}."""

        return prompt

    def generate_csv_with_gpt(self, result):
        csv_data = self.csvLayout.loadedCSVData
        checkboxes_values = self.formLayout.checkboxesValues

        if csv_data is None:
            return

        output_lines = []

        for index, line in enumerate(csv_data):
            try:
                gpt_response = result[index]

                data = gpt_response.replace('\n', '')

                json_pattern = r'{.*}'
                match = re.search(json_pattern, data)
                if match:
                    json_parsed = json.loads(match.group(0))
                    if checkboxes_values.get("fullDescription"):
                        line["_LONG_DESCRIPTION_"] = json_parsed["text"]

                    if checkboxes_values.get("title"):
                        line["_META_TITLE_"] = json_parsed["title"]

                    if checkboxes_values.get("h1"):
                        line["_META_H1_"] = json_parsed["h1"]

                    if checkboxes_values.get("description"):
                        line["_DESCRIPTION_"] = json_parsed["description"]

                    if checkboxes_values.get("keywords"):
                        line["_SEO_KEYWORD_"] = json_parsed["keywords"]

                    output_lines.append(line)

                else:
                    print('No JSON found in the text.')
            except ValueError:
                print("Error while reading JSON!")

        headers = ["_ID_", "_CATEGORY_", "_NAME_", "_MANUFACTURER_", "_PRICE_", "_META_TITLE_", "_META_H1_",
                   "_DESCRIPTION_", "_SEO_KEYWORD_", "_DISCOUNT_", "_SPECIAL_", "_ATTRIBUTES_",
                   "_LONG_DESCRIPTION_"]

        write_to_csv("output.csv", headers, output_lines)

    def get_gpt_prompts(self):
        csv_data = self.csvLayout.loadedCSVData
        prompts = []
        if csv_data is None:
            return []

        for line in csv_data:
            prompts.append(self.get_prompt_for_line(line))

        return prompts

    def report_progress(self):
        self.formLayout.progressBar.raw_progress += 1

        max_progress = len(self.csvLayout.loadedCSVData)
        percent_progress = int(self.formLayout.progressBar.raw_progress / max_progress * 100)

        if percent_progress > 100:
            percent_progress = 100

        self.formLayout.progressBar.setValue(percent_progress)

    def send_requests(self):
        self.thread = QtCore.QThread()
        self.worker = GPTWorker(self.get_gpt_prompts())
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.finished.connect(self.generate_csv_with_gpt)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.report_progress)
        self.thread.start()

        self.formLayout.generateButton.setEnabled(False)
        self.csvLayout.loadCSVButton.setEnabled(False)
        self.formLayout.progressBar.raw_progress = 0
        self.formLayout.progressBar.setValue(0)

        self.thread.finished.connect(self.finish_loading)

    def finish_loading(self):
        self.formLayout.generateButton.setEnabled(True)
        self.csvLayout.loadCSVButton.setEnabled(True)
