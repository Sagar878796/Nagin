import json
import requests
import re

BASE_URL = "https://sayan-sportlink-jio-tv-main.pages.dev"

json_url = f"{BASE_URL}/Channel/channels.json"
channels = requests.get(json_url).json()

m3u = "#EXTM3U\n\n"

for ch in channels:
    try:
        name = ch.get("name", "Unknown")
        logo = ch.get("logo", "")
        group = ch.get("category", "Live TV")
        file_name = ch.get("fileName", "")

        page_url = f"{BASE_URL}/{file_name}"

        html = requests.get(page_url, timeout=10).text

        stream = None

        patterns = [
            r'https?://[^"\']+\.m3u8[^"\']*',
            r'https?://[^"\']+\.mpd[^"\']*'
        ]

        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                stream = match.group(0)
                break

        if stream:
            m3u += (
                f'#EXTINF:-1 tvg-name="{name}" '
                f'tvg-logo="{logo}" '
                f'group-title="{group}",{name}\n'
            )
            m3u += stream + "\n\n"

            print(f"Added: {name}")

    except Exception as e:
        print(f"Error: {e}")

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("playlist.m3u generated")
