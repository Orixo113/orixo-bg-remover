from flask import Flask, request, send_file, send_from_directory
import requests
import io

app = Flask(__name__)

API_KEY = "m2vJqo5FxNTMbBYLTEdsEwkp"

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/logo.png')
def logo():
    return send_from_directory('.', 'logo.png')


@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    file = request.files.get('image')

    if not file:
        return "No file", 400

    response = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        files={"image_file": file.stream},
        data={"size": "auto"},
        headers={"X-Api-Key": API_KEY},
    )

    if response.status_code == 200:
        return send_file(io.BytesIO(response.content), mimetype='image/png')
    else:
        return response.text, 500


if __name__ == "__main__":
    app.run(debug=True)