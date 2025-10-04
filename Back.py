# here we are importing the necessary libraries for our backend.
# flask will help us create the web server.
# requests will be used to talk to the hugging face api.
# os and dotenv are for securely loading our api key.
# cors will let our frontend talk to our backend.
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# here we enable cross-origin resource sharing (cors)
# this is important so our github pages site can send requests to this server.
CORS(app)

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"

@app.route('/summarize', methods=['POST'])
def summarize():
    # we get the json data sent from the frontend.
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'no text provided in request.'}), 400

    text_to_summarize = data['text']
    
    if not HUGGINGFACE_API_KEY:
        return jsonify({'error': 'HUGGINGFACE_API_KEY not configured on the server.'}), 500

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }

    payload = {
        "inputs": text_to_summarize,
        "parameters": {
            "min_length": 60,
            "max_length": 150,
        }
    }

    # now, our python server calls the hugging face api, not the frontend.
    try:
        response = requests.post(HUGGINGFACE_API_URL, headers=headers, json=payload)
        response.raise_for_status() # this will raise an http error for bad responses (4xx or 5xx)
        summary = response.json()
        return jsonify(summary)
    except requests.exceptions.HTTPError as http_err:
        # we can provide more specific error messages here.
        if "is currently loading" in response.text:
            return jsonify({'error': 'the summarization model is starting up. please wait a moment and try again.'}), 503
        return jsonify({'error': f'http error occurred: {http_err}', 'details': response.text}), response.status_code
    except Exception as err:
        return jsonify({'error': f'an other error occurred: {err}'}), 500

if __name__ == '__main__':
    # this lets us run the server locally for testing.
    app.run(debug=True, port=5000)
