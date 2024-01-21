from flask import Flask, request, jsonify, render_template
import openai
from openai import OpenAI

from dotenv import load_dotenv
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Configuration et initialisation des clients API
load_dotenv()
client = OpenAI()

client.api_key = os.environ.get("OPENAI_API_KEY")
mistral_api_key = os.environ["MISTRAL_API_KEY"]
mistral_model = "mistral-medium"

mistral_client = MistralClient(api_key=mistral_api_key)

app = Flask(__name__)

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data['message']

    messages = [{"role": "user", "content": user_message}]

    # Réponse de OpenAI
    openai_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0
    ).choices[0].message.content

    # Réponse de Mistral
    mistral_messages = [
        ChatMessage(role="user", content=user_message)
    ]
    mistral_response = mistral_client.chat(
        model=mistral_model,
        messages=mistral_messages,
    ).choices[0].message.content

    return jsonify({"openai_response": openai_response, "mistral_response": mistral_response})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

