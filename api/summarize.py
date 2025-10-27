import google.generativeai as genai
import os
import json
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode())

        text = data.get("text", "").strip()
        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "No text provided"}).encode())
            return

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing GEMINI_API_KEY"}).encode())
            return

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        try:
            prompt = f"Summarize this text in 3–4 lines:\n\n{text}"
            response = model.generate_content(prompt)
            summary = response.text.strip()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"summary": summary}).encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
