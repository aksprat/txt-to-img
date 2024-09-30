from flask import Flask, request, jsonify, send_file
import requests
from io import BytesIO

app = Flask(__name__)

# Hugging Face API endpoint and authorization
HF_API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HF_API_KEY = "Bearer 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"

@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get("prompt")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    headers = {
        "Authorization": HF_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt, "options": {"wait_for_model": True}})
    
    if response.status_code == 200:
        image_data = response.content
        return send_file(BytesIO(image_data), mimetype="image/png")
    else:
        return jsonify({"error": "Failed to generate image"}), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
