import requests

def get_json_with_requests(url):
    cookies = {
        'relevanceUser': '005009916225510713',
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:143.0) Gecko/20100101 Firefox/143.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.olx.in/gurgaon_g4058748/q-ps4',
        # 'X-Panamera-fingerprint': 'cd4b6e9eec9bb3bddf32fd68ccd7b30e#1778352737917',
        'Origin': 'https://www.olx.in',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Priority': 'u=0',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # print(response.text)
    return response.json()

if __name__ == '__main__':
    get_json_with_requests("https://api.olx.in/relevance/v4/search?facet_limit=1000&lang=en-IN&location=4058748&location_facet_limit=40&platform=web-desktop&pttEnabled=true&query=ps4&relaxedFilters=true&size=500&spellcheck=true&user=005009916225510713&price_max=35000&price_min=12000")
    print("exiting!")