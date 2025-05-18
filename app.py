from flask import Flask, request
import requests
import openai
import os

app = Flask(__name__)

VERIFY_TOKEN = 'badboy2025'  # <-- bạn có thể đổi
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')  # <-- bạn thay bằng token của Fanpage
OPENAI_API_KEY = 'sk-...YOUR_OPENAI_KEY...'  # <-- bạn thay bằng OpenAI key

openai.api_key = OPENAI_API_KEY

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Token sai", 403

    if request.method == 'POST':
        data = request.get_json()
        if 'entry' in data:
            for entry in data['entry']:
                for event in entry.get('messaging', []):
                    sender_id = event['sender']['id']
                    if 'message' in event and 'text' in event['message']:
                        user_message = event['message']['text']
                        reply = generate_reply(user_message)
                        send_message(sender_id, reply)
        return "ok", 200

def generate_reply(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một chàng trai hài hước, lãng mạn và bad boy nhẹ chuyên tán gái."},
                {"role": "user", "content": user_input}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return "Anh hơi lag tí, nhắn lại được không bé 😅"

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

if __name__ == '__main__':
    app.run(debug=True)
