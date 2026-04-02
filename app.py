from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='static')

# 🔑 YOUR API KEY
API_KEY = "wDn2ZQT62wp8447rrK9XyDTE"

# 📁 ensure static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

# 🏠 Home Route
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')


# 🎯 Background Remove Route
@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'image' not in request.files:
            return jsonify({"status": "error", "message": "No image uploaded"})

        file = request.files['image']

        # 🔥 API CALL
        response = requests.post(
            "https://api.remove.bg/v1.0/removebg",
            files={"image_file": file.stream},   # IMPORTANT FIX
            data={"size": "auto"},
            headers={"X-Api-Key": API_KEY},
        )

        # 🔍 DEBUG PRINT (CMD me dikhega)
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)

        if response.status_code == 200:
            output_path = "static/output.png"

            with open(output_path, "wb") as f:
                f.write(response.content)

            return jsonify({
                "status": "success",
                "image_url": "/static/output.png"
            })

        else:
            return jsonify({
                "status": "error",
                "message": response.text   # REAL ERROR SHOW
            })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })


# 📂 Static file serve
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# 🚀 RUN SERVER
if __name__ == '__main__':
    app.run(debug=True)