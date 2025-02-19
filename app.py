import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow requests from Moodle

import os

# Hugging Face API Key (Replace with your key)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

@app.route('/chat', methods=['GET'])
def chat():
    # Get course content from Moodle
    course_content = request.args.get('course_content', 'No content available')

    # Construct AI prompt
    prompt = f"""
    You are an AI tutor helping students with their courses.
    The student is currently studying the following topic:

    "{course_content}"

    Provide a **detailed and structured** explanation of this topic.
    """

    # Call Hugging Face's Free AI Model
    response = requests.post(
        "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct",
        headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
        json={"inputs": prompt}
    )

    # Get AI response
    ai_response = response.json()
    message = ai_response[0]["generated_text"] if isinstance(ai_response, list) else "Error generating response."

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
