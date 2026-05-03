import requests

url = "https://allinonereborn.online/jtv-fetch/jstr4web.json"
data = requests.get(url).json()

m3u = "#EXTM3U\n\n"

# JSON structure dynamic ho sakta hai
for ch in data:
    name = ch.get("name") or ch.get("title") or "No Name"
    logo = ch.get("logo") or ch.get("image") or ""
    group = ch.get("group") or ch.get("category") or "Live TV"
    url = ch.get("url") or ch.get("link") or ch.get("stream") or ""

    if url:
        m3u += f'#EXTINF:-1 tvg-logo="{logo}" group-title="{group}",{name}\n'
        m3u += f"{url}\n\n"

with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write(m3u)

print("✅ M3U Generated")
