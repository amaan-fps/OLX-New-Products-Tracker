import os
from telegram_alert.telegram_alert import send_telegram_alerts
from dotenv import load_dotenv
import asyncio
from ads_scraper import start_requests

load_dotenv()

# Paths
SEARCH_TERMS_FILE = os.path.join('add_queries', 'search_terms.json')
SEEN_ADS_FILE = 'seen_ads.json'
NEW_ADS_FILE = 'new_ads_data.json'

async def run_tracker():
    # user_choice = input("Do you want to add new queries to the tracker (optional), press y/n")
    # match user_choice:
    #     case 'y':
    #         add_new_search_term()
    #     case 'n':
    start_requests()
    print("new data fetched, sending alert for any new data...")
    await send_telegram_alerts()

if __name__ == '__main__':
    asyncio.run(run_tracker())
