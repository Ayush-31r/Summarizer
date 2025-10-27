import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)
genai.configure(api_key="AIzaSyDp7OjdH7q9LSzvUn-Z6zBQ_RIKYQLXmwk")  # replace with your key
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400

    prompt = f"Summarize the following text in 3-4 lines, keeping the key information only:\n\n{text}"
    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)