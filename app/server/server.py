# server.py
from flask import Flask, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/data/chart/<filename>")
def send_vega_lite_file(filename):
    print(f"filename: {filename}")
    return send_from_directory("data/chart", filename)


if __name__ == "__main__":
    app.run(debug=True, port=5678)
