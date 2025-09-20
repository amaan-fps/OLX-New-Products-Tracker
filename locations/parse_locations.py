import requests
import re
import json
from bs4 import BeautifulSoup

def fetch_and_parse_locations():
    url = "https://www.olx.in/locations.xml"
    # Fetch the sitemap
    cookies = {
        'panoramaId': 'c2c0535c3637edce12472000c4bf185ca02c51e872941e06367c1bdabe3142b1',
        'relevanceUser': '005009916225510713',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch sitemap {response.status_code}")
        exit()

    locations = []
    # Parse XML
    soup = BeautifulSoup(response.content, "xml")
    # product_urls = []
    for url_tag in soup.find_all("url"):
        loc_tag = url_tag.find("loc")
        if loc_tag:
            loc_url = loc_tag.text.strip()
            match = re.search(r"https://www\.olx\.in/([^_]+)_g(\d+)", loc_url)

            if match:
                name = match.group(1).replace('-', ' ').title()
                id_ = match.group(2)
                locations.append({
                    "name": name,
                    "id": id_,
                    "url_slug": f"{match.group(1)}_g{id_}"
                })

    with open("locations.json", "w") as f:
        json.dump(locations, f, indent=2)

    print(f"{len(locations)} locations saved to locations.json")

if __name__ == "__main__":
    fetch_and_parse_locations()
