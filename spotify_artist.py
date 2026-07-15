from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = "https://open.spotify.com/"
driver.get(url)

input("Đăng nhập Spotify rồi nhấn Enter...")

time.sleep(5)

artists = []

artist_links = driver.find_elements(
    By.CSS_SELECTOR,
    'a[href^="/artist/"]'
)

seen = set()

for artist in artist_links:
    try:
        name = artist.get_attribute("title") or artist.text.strip()

        href = artist.get_attribute("href")

        if not href:
            continue

        artist_id = href.split("/artist/")[-1].split("?")[0]

        if artist_id in seen:
            continue

        seen.add(artist_id)

        avatar = ""

        try:
            card = artist.find_element(
                By.XPATH,
                "./ancestor::*[@data-testid='home-card']"
            )

            img = card.find_element(By.TAG_NAME, "img")
            avatar = img.get_attribute("src")

        except:
            pass

        artists.append({
            "artist_id": artist_id,
            "artist_name": name,
            "artist_url": href,
            "avatar_url": avatar
        })

        print(f"[{len(artists)}] {name} - {artist_id}")

    except Exception as e:
        print("Lỗi:", e)

driver.quit()

with open(
    "spotify_artists.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "artist_id",
            "artist_name",
            "artist_url",
            "avatar_url"
        ]
    )

    writer.writeheader()
    writer.writerows(artists)

print(f"\nĐã lưu {len(artists)} nghệ sĩ")