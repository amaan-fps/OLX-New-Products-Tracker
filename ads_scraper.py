import json
import os
from urllib.parse import urlencode
from requests_check import get_json_with_requests

def start_requests():
    base_url = "https://www.olx.in/api/relevance/v4/search"

    with open('add_queries/search_terms.json', 'r') as file:
        all_queries = json.load(file)

    print(f"Tracking changes in {len(all_queries)} keywords...")

    new_ads = []

    for query in all_queries:
        location_id = query['location_id']
        location_name = query['location_name']
        search_term = query['query']
        max_price = query['max_price']
        min_price = query['min_price']

        params = {
            "facet_limit": 1000,
            "lang": "en-IN",
            "location": location_id,
            "location_facet_limit": 40,
            #"page": page,
            "platform": "web-desktop",
            "pttEnabled": "true",
            "query": search_term,
            "relaxedFilters": "true",
            "size": 500,
            "spellcheck": "true",
            "user": "005009916225510713",
            "price_max": max_price,
            "price_min": min_price,
        }

        query_string = urlencode(params)
        full_url = f"{base_url}?{query_string}"

        print(full_url)

        json_data = get_json_with_requests(full_url)

        seen_ads = load_seen_ads()
        seen_key = f"{search_term.lower()} - {location_id}"
        seen_ids = seen_ads.get(seen_key, [])

        new_ids = []

        try:
            results = json_data.get('data', [])
            print(f"✅ Fetched {len(results)} ads.\nChecking for New ads...")

            is_first_time = seen_key not in seen_ads
            if is_first_time:
                print(f"🆕 New query detected: {seen_key} — skipping alerts.")
                # Save all current ad_ids to avoid alerting on next run
                updated_seen = [str(ad.get('ad_id')) for ad in results][:MAX_SEEN]
                seen_ads[seen_key] = updated_seen
                save_seen_ads(seen_ads)
                continue  # Skip to the next query

            for ad in results:
                ad_id = str(ad.get('ad_id'))
                if ad_id not in seen_ids:
                    new_ads.append(ad)
                    new_ids.append(ad_id)

            # update seen list
            print("Updating Ads list...")
            updated_seen = (new_ids + seen_ids)[:MAX_SEEN]
            seen_ads[seen_key] = updated_seen
            save_seen_ads(seen_ads)
            save_new_ads(new_ads)

        except Exception as e:
            print(f"Error parsing results {seen_key}: {e}")

SEEN_ADS_FILE = 'seen_ads.json'
MAX_SEEN = 1000  # how many old ads to keep per query-location

def load_seen_ads():
    if not os.path.exists(SEEN_ADS_FILE):
        return {}
    try:
        with open(SEEN_ADS_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_seen_ads(data):
    with open(SEEN_ADS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def save_new_ads(data):
    with open('new_ads_data.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    start_requests()
    print("Done Fetching Results")
