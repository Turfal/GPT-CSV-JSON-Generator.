from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import csv
import json
import re
import concurrent.futures
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
openai.api_key = "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"


def write_to_csv(filename, headers, data):
    with open(filename, 'w', newline='', encoding="utf-8-sig") as csv_file:
        csv_writer = csv.DictWriter(csv_file, headers, delimiter=";")
        csv_writer.writeheader()
        csv_writer.writerows(data)

        print(f"Write successful {len(data)} rows")

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

def process_file(file_path, language, comment, tags):
    # Load data from the CSV file
    with open(file_path, newline='', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f, delimiter=';')
        csv_data = list(reader)

    # Prepare GPT-3 prompts for each line in the CSV
    prompts = []
    for line in csv_data:
        if line["_DESCRIPTION_"] != "":
            help_text = line["_DESCRIPTION_"]
        else:
            help_text = line["_NAME_"]

        help_text += f". {comment}"

        prompt = f"""
        Сгенерируй JSON-ответ на основе следующего текста:

        {help_text}

        Формат JSON-ответа - JSON следующего вида, где "text" - описание товара, рерайт переданного 
        текста (оптимальный объем текста 400-800 символов), "h1" - текст для html тэга H1,  
        "title" - текст для html мета-тэга title, "description" - текст для html мета-тэга description (
        рекомендуемая длина 160-170 символов), "keywords" - текст для html мета-тэга keywords (
        разделитель - запятая): 
        {{ 
        "text": "",
        "h1": "",
        "title": "",
        "description": "",
        "keywords": ""
        }}

        Язык всего генерируемого текста: {language}."""

        prompts.append(prompt)

    # Process GPT-3 prompts using multiple threads
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(create_gpt_completion, prompt) for prompt in prompts]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    # Update CSV data with generated JSON responses
    output_lines = []
    for index, line in enumerate(csv_data):
        try:
            gpt_response = results[index]
            data = gpt_response.replace('\n', '')
            json_pattern = r'{.*}'
            match = re.search(json_pattern, data)
            if match:
                json_parsed = json.loads(match.group(0))
                if "fullDescription" in tags:
                    line["_LONG_DESCRIPTION_"] = json_parsed["text"]
                if "title" in tags:
                    line["_META_TITLE_"] = json_parsed["title"]
                if "h1" in tags:
                    line["_META_H1_"] = json_parsed["h1"]
                if "description" in tags:
                    line["_DESCRIPTION_"] = json_parsed["description"]
                if "keywords" in tags:
                    line["_SEO_KEYWORD_"] = json_parsed["keywords"]
            else:
                print(f"No JSON found in the GPT-3 response for line {index + 1}")
        except ValueError:
            print(f"Error while reading JSON for line {index + 1}")
        output_lines.append(line)

    # Write updated data to a new CSV file
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "output.csv")
    headers = csv_data[0].keys()
    write_to_csv(output_file_path, headers, output_lines)

    return output_file_path


@app.route('/message')
def message():
    return render_template('result.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    processed_file = None

    if request.method == 'POST':
        file = request.files['csv_file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            language = request.form.get('language')
            comment = request.form.get('comment')
            tags = request.form.getlist('tags')
            output_file_path = process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), language, comment, tags)

            # Set the processed_file variable to the path of the processed file
            processed_file = output_file_path

            # Redirect to the message page
            return redirect(url_for('message'))

    return render_template('index.html', processed_file=processed_file)

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('uploads/'):
        os.makedirs('uploads/')
    app.run(debug=True)