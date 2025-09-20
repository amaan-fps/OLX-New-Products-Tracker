import requests

def get_json_with_requests(url):
    cookies = {
        'relevanceUser': '005009916225510713',
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Microsoft Edge";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0',
    }

    response = requests.get(url, cookies=cookies, headers=headers)
    response.raise_for_status()

    return response.json()

if __name__ == '__main__':
    get_json_with_requests("https://www.olx.in/api/relevance/v4/search?facet_limit=1000&lang=en-IN&location=4058748&location_facet_limit=40&platform=web-desktop&pttEnabled=true&query=ps4&relaxedFilters=true&size=500&spellcheck=true&user=005009916225510713&price_max=13000&price_min=3000")
    print("exiting!")