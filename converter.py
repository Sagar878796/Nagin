import requests
import re
from bs4 import BeautifulSoup

BASE_URL = "https://sayan-sportlink-jio-tv-main.pages.dev"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Get channels
channels = requests.get(
    f"{BASE_URL}/Channel/channels.json",
    headers=headers
).json()

m3u = "#EXTM3U\n\n"

found = 0

for ch in channels[:200]:

    try:
        name = ch.get("name", "Unknown")
        logo = ch.get("logo", "")
        category = ch.get("category", "Live TV")
        file_name = ch.get("fileName", "")

        url = f"{BASE_URL}/{file_name}"

        print(f"Checking: {name}")

        r = requests.get(url, headers=headers, timeout=10)
        html = r.text

        soup = BeautifulSoup(html, "html.parser")

        stream = None

        # 1. Search full HTML
        matches = re.findall(
            r'https?://[^\s"\']+',
            html
        )

        for m in matches:
            if ".m3u8" in m or ".mpd" in m:
                stream = m
                break

        # 2. Search iframe
        if not stream:
            iframe = soup.find("iframe")

            if iframe and iframe.get("src"):

                iframe_url = iframe.get("src")

                if iframe_url.startswith("/"):
                    iframe_url = BASE_URL + iframe_url

                print("Iframe:", iframe_url)

                iframe_html = requests.get(
                    iframe_url,
                    headers=headers,
                    timeout=10
                ).text

                iframe_matches = re.findall(
                    r'https?://[^\s"\']+',
                    iframe_html
                )

                for m in iframe_matches:
                    if ".m3u8" in m or ".mpd" in m:
                        stream = m
                        break

        # Save
        if stream:

            found += 1

            print("FOUND:", stream)

            m3u += (
                f'#EXTINF:-1 tvg-name="{name}" '
                f'tvg-logo="{logo}" '
                f'group-title="{category}",{name}\n'
            )

            m3u += stream + "\n\n"

    except Exception as e:
        print("ERROR:", e)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print(f"DONE - Found {found} streams")
