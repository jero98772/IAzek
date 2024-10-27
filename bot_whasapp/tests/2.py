from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Retrieving incoming message
    incoming_message = request.json
    print(incoming_message)
    # Retrieving the text of the message
    message_text = incoming_message.get('body', '').lower()

    # Deciding the reply based on the command
    if message_text == 'hello':
        response_text = 'Hi! How can I assist you today?'
    elif message_text == 'info':
        response_text = 'I am a WhatsApp bot created to assist you!'
    else:
        response_text = 'I am sorry, I do not understand the command.'

    # Sending the reply message
    send_message(response_text, incoming_message['from'])

    return '', 200

def send_message(response_text, to):
    # URL to send messages through the Whapi.Cloud API
    url = "https://gate.whapi.cloud/messages/text?token=TOKEN"

    # Forming the body of the message
    payload = {
        "to": to,
        "body": response_text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    # Sending the message
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
