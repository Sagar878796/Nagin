import requests
import re
import json

BASE_URL = "https://sayan-sportlink-jio-tv-main.pages.dev"

json_url = f"{BASE_URL}/Channel/channels.json"
channels = requests.get(json_url).json()

m3u = "#EXTM3U\n\n"

headers = {
    "User-Agent": "Mozilla/5.0"
}

for ch in channels[:100]:

    try:
        name = ch.get("name", "Unknown")
        logo = ch.get("logo", "")
        group = ch.get("category", "Live TV")
        file_name = ch.get("fileName", "")

        page_url = f"{BASE_URL}/{file_name}"

        print("Checking:", name)

        html = requests.get(page_url, headers=headers, timeout=5).text

        urls = re.findall(
            r'https?://[^\s"\']+\.(m3u8|mpd)[^\s"\']*',
            html
        )

        real_urls = re.findall(
            r'https?://[^\s"\']+',
            html
        )

        stream = None

        for u in real_urls:
            if ".m3u8" in u or ".mpd" in u:
                stream = u
                break

        if stream:
            print("FOUND:", stream)

            m3u += (
                f'#EXTINF:-1 tvg-name="{name}" '
                f'tvg-logo="{logo}" '
                f'group-title="{group}",{name}\n'
            )

            m3u += stream + "\n\n"

    except Exception as e:
        print("ERROR:", e)

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("DONE")
