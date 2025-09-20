# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import json
from dotenv import load_dotenv

load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
FROM = os.environ["TWILIO_FROM"]
TO = os.environ["TWILIO_TO"]


def send_whatsapp_message(body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=FROM,
        to=TO
    )
    print(f"✅ WhatsApp message sent. SID: {message.sid}")

def load_new_ads():
    if not os.path.exists('../new_ads_data.json'):
        print("❌ new_ads_data.json not found.")
        return []

    with open('../new_ads_data.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON.")
            return []

def format_message(ad):
    title = ad.get("title", "No Title")
    price = ad.get("price", {}).get("value", {}).get("raw", "empty")
    desc = ad.get("description", "Empty Description")
    link = f"https://www.olx.in/item/{ad.get("ad_id", "-")}"

    message = f"🆕 New OLX Ad:\n\n📌 {title}\n💰 Price: ₹{price}\n📝 {desc[:100]}...\n🔗 {link}"
    return message

if __name__ == '__main__':
    ads = load_new_ads()

    if not ads:
        print("📭 No new ads to send.")
    else:
        print(f"📬 Found {len(ads)} new ads. Sending alerts...")
        for ad in ads:
            msg = format_message(ad)
            send_whatsapp_message(msg)