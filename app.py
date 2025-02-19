import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Allow requests from Moodle


load_dotenv()

# Hugging Face API Key (Replace with your key)
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is not set. Please add it as an environment variable.")

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
    if isinstance(ai_response, list) and len(ai_response) > 0:
        message = ai_response[0].get("generated_text", "Error generating response.")
    elif isinstance(ai_response, dict):
        message = ai_response.get("generated_text", "Error generating response.")
    else:
        message = "Error generating response."

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
