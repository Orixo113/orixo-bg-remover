from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__)

# 🔑 API KEY (yahi change hota hai)
API_KEY = "wDn2ZQT62wp8447rrK9XyDTE"

# folders
UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    if "image" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["image"]
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = os.path.join(STATIC_FOLDER, "output.png")

    # 🔥 REMOVE.BG API CALL
    with open(input_path, "rb") as img:
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": img},
            data={"size": "auto"},
            headers={"X-Api-Key": API_KEY},
        )

    # ❗ ERROR CHECK
    if response.status_code != 200:
        print("ERROR:", response.text)
        return jsonify({"error": "Remove.bg API error"})

    # save output
    with open(output_path, "wb") as out:
        out.write(response.content)

    return jsonify({"output": "/static/output.png"})


# static files serve
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)


if __name__ == "__main__":
    app.run(debug=True)