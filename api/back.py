from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

# Load environment variable
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "backend is running."})

@app.route("/api/back/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "no text provided in request."}), 400

    text_to_summarize = data["text"]

    if not HUGGINGFACE_API_KEY:
        return jsonify({"error": "HUGGINGFACE_API_KEY not configured."}), 500

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": text_to_summarize, "parameters": {"min_length": 60, "max_length": 150}}

    try:
        
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.HTTPError as http_err:
        if "is currently loading" in response.text:
            return jsonify({"error": "model is starting up, try again later."}), 503
        return jsonify({"error": f"http error: {http_err}", "details": response.text}), response.status_code
    except Exception as err:
        return jsonify({"error": f"an error occurred: {err}"}), 500
