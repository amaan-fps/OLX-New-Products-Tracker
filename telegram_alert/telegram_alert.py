from telegram import Bot
import json
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

TELE_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")  # Your user ID or a group ID

bot = Bot(token=TELE_TOKEN)

def load_new_ads():
    if not os.path.exists('new_ads_data.json'):
        print("❌ new_ads_data.json not found.")
        return []
    with open('new_ads_data.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("❌ JSON decode error.")
            return []

def format_message(ad):
    title = ad.get("title", "No Title")
    price = ad.get("price", {}).get("value", {}).get("raw", "N/A")
    desc = ad.get("description", "No Description")
    link = f"https://www.olx.in/item/{ad.get('ad_id', '-')}"
    text = f"🆕 *{title}*\n💰 Price: ₹{price}\n📝 {desc[:100]}...\n🔗 [View Ad]({link})"
    return text

async def send_telegram_alerts():
    ads = load_new_ads()
    if not ads:
        print("📭 No new ads to send.")
        return

    for ad in ads:
        msg = format_message(ad)
        try:
            await bot.send_message(chat_id=CHAT_ID, text=msg, parse_mode='Markdown', disable_web_page_preview=True)
            print("✅ Sent message for ad:", ad.get("title"))
        except Exception as e:
            print("❌ Error sending message:", e)

if __name__ == "__main__":
    asyncio.run(send_telegram_alerts())
