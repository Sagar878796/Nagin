import requests

JSON_URL = "https://steep-silence-90df.sagarsutradhar046.workers.dev/"

channels = requests.get(JSON_URL).json()

m3u = "#EXTM3U\n\n"

for ch in channels:

    name = ch.get("name", "Unknown")
    logo = ch.get("logo", "")
    group = ch.get("category", "Live TV")
    file_name = ch.get("fileName", "")

    url = (
        "https://sayan-sportlink-jio-tv-main.pages.dev/"
        + file_name
    )

    m3u += (
        f'#EXTINF:-1 tvg-name="{name}" '
        f'tvg-logo="{logo}" '
        f'group-title="{group}",{name}\n'
    )

    m3u += url + "\n\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("playlist.m3u created")
