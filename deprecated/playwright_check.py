import asyncio
from playwright.async_api import async_playwright

async def fetch_json_from_url(url: str) -> dict:
    async with async_playwright() as p:
        #browser = await p.chromium.launch(headless=True)  # Set headless=False to see the browser
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--no-sandbox",
            ]
        )
        #context = await browser.new_context()
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
            ignore_https_errors=True,
        )
        page = await context.new_page()

        # Set stealthy headers
        await page.set_extra_http_headers({
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.olx.in/",
        })

        print(f"Opening URL: {url}")
        response = await page.goto(url, wait_until="networkidle")

        # Wait for 2 seconds so you can see the browser (optional)
        await page.wait_for_timeout(2000)

        if response.status != 200:
            raise Exception(f"Failed to fetch JSON. Status: {response.status}")

        # Get response JSON
        if response:
            json_data = await response.json()
            print(f"Response JSON received")
        else:
            json_data = {}
            print("No response received")

        await browser.close()
        return json_data

def get_json(url: str) -> dict:
    """Sync wrapper for easier use in normal scripts."""
    return asyncio.run(fetch_json_from_url(url))

if __name__ == '__main__':
    get_json("https://www.olx.in/api/relevance/v4/search?facet_limit=1000&lang=en-IN&location=4058748&location_facet_limit=40&platform=web-desktop&pttEnabled=true&query=ps4&relaxedFilters=true&size=500&spellcheck=true&user=005009916225510713&price_max=13000&price_min=3000")
    print("exiting!")