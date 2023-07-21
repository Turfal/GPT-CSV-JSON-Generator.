# GPT-3 Flask App

This is a simple web application built with Flask that demonstrates how to use the OpenAI GPT-3 API to generate JSON responses based on input text. The app allows users to upload a CSV file containing text data, select options for language and tags, and then process the file using GPT-3 to generate JSON responses. Once processed, the app provides a link to download the output CSV file with the generated JSON responses.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python (tested on Python 3.7+)
- Flask
- OpenAI GPT-3 API Key

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/gpt3-flask-app.git
   cd gpt3-flask-app
   ```

2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Obtain your OpenAI GPT-3 API key from the OpenAI website.

2. Open the `app.py` file in a text editor and replace `"YOUR_GPT3_API_KEY"` with your actual API key:

   ```python
   openai.api_key = "YOUR_GPT3_API_KEY"
   ```

3. Run the Flask app:

   ```bash
   python app.py
   ```

4. Access the web application in your web browser at `http://127.0.0.1:5000/`.

5. On the web page, upload a CSV file containing the text data you want to process.

6. Select the language and tags options based on your requirements.

7. Click the "Generate JSON" button to initiate the processing using GPT-3.

8. Once the file is processed, a link to download the output CSV file will appear.

## Folder Structure

- `app.py`: The main Flask application that handles file uploading, processing, and generating JSON responses using GPT-3.
- `uploads/`: The folder to store uploaded CSV files and the output CSV file with generated JSON responses.
- `templates/`: Contains the HTML templates used for rendering the web pages.
- `static/`: Contains CSS and JavaScript files for styling and client-side interactions.

## Contributing

Contributions are welcome! If you find any issues or want to enhance the functionality of the app, feel free to open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
