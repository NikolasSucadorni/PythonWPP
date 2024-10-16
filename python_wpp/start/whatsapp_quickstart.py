import json
from dotenv import load_dotenv
import os
import requests
import aiohttp
import asyncio

# --------------------------------------------------------------
# Variáveis
# --------------------------------------------------------------

load_dotenv(dotenv_path=r'python-whatsapp-bot\.env')
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
print(f"RECIPIENT_WAID: {RECIPIENT_WAID}")
print(f"PHONE_NUMBER_ID: {PHONE_NUMBER_ID}")
print(f"VERSION: {VERSION}")

# --------------------------------------------------------------
# Envio de mensagem template
# --------------------------------------------------------------


def send_whatsapp_message():
    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": "Bearer " + ACCESS_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "messaging_product": "whatsapp",
        "to": RECIPIENT_WAID,
        "type": "template",
        "template": {"name": "Apresentação", "language": {"code": "pt_BR"}},
    }
    response = requests.post(url, headers=headers, json=data)
    return response


# Chamada da Def
response = send_whatsapp_message()
print(response.status_code)
print(response.json())

# --------------------------------------------------------------
# Envio de mensagem customizada
# --------------------------------------------------------------


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    url = f"https://graph.facebook.com/{VERSION}/{PHONE_NUMBER_ID}/messages"

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Status:", response.status_code)
        print("Content-type:", response.headers["content-type"])
        print("Body:", response.text)
        return response
    else:
        print(response.status_code)
        print(response.text)
        return response


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Olá, esta é uma mensagem de teste."
)

response = send_message(data)

# --------------------------------------------------------------
# Envio mensagem async
# OBS: Não testar no Jupyter! Não irá funcionar.
# --------------------------------------------------------------

async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }

    async with aiohttp.ClientSession() as session:
        url = "https://graph.facebook.com" + f"/{VERSION}/{PHONE_NUMBER_ID}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    print("Status:", response.status)
                    print("Content-type:", response.headers["content-type"])

                    html = await response.text()
                    print("Body:", html)
                else:
                    print(response.status)
                    print(response)
        except aiohttp.ClientConnectorError as e:
            print("Connection Error", str(e))


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


data = get_text_message_input(
    recipient=RECIPIENT_WAID, text="Olá, esta é uma mensagem de teste."
)

loop = asyncio.get_event_loop()
loop.run_until_complete(send_message(data))
loop.close()
