
import requests

url = "https://gate.whapi.cloud/messages/text?token=TOKEN"

payload = {
    "typing_time": 5,
    "to": "1234567891@s.whatsapp.net",
    "body": "Hello, world!"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)

