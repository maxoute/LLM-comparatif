from flask import Flask, request, jsonify, render_template
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
from dotenv import load_dotenv
import os
load_dotenv()


from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-tiny"

client = MistralClient(api_key=api_key)

messages = [
    ChatMessage(role="user", content="What is the best French cheese?")
]

# No streaming
chat_response = client.chat(
    model=model,
    messages=messages,
)

# With streaming
for chunk in client.chat_stream(model=model, messages=messages):
    print(chunk)

















app = Flask(__name__)
messages = [{"role": "system", 
             "content": "You are an intelligent assistant, tu réponds qu'au question en rapport avec le foot et si tu ne sais pas dis que tu ne sais pas"},
            {"role": "user", "content": "Hello! je voudrais te poser des questions sur le foootball"}]

@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.json
    user_message = data['message']
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(model="ft:gpt-3.5-turbo-0613:amaris:model-trainin:8DZrJTRv",
    messages=messages,
    temperature=0)
    
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    return jsonify({"response": response.choices[0].message.content})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
