from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

driver = webdriver.Chrome()

artist_url = "https://open.spotify.com/artist/27RoKwun6jKycKbH2iYUFU"

driver.get(artist_url)

wait = WebDriverWait(driver,20)

try:
    see_more = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(.,'See more') or contains(.,'Hiện thêm') or contains(.,'Xem thêm')]"
            )
        )
    )

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", see_more)
    driver.execute_script("arguments[0].click();", see_more)

except:
    print("Không tìm thấy nút See more")

wait.until(
    EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR,'div[data-testid="tracklist-row"]')
    )
)

rows = driver.find_elements(By.CSS_SELECTOR,'div[data-testid="tracklist-row"]')

artist_id = artist_url.split("/")[-1]

data = []

for row in rows[:10]:

    link = row.find_element(By.CSS_SELECTOR,'a[data-testid="internal-track-link"]')

    track_url = link.get_attribute("href")

    track_id = track_url.split("/")[-1]

    name = link.text

    image = row.find_element(By.TAG_NAME,"img").get_attribute("src")

    playcount = row.find_element(
        By.CSS_SELECTOR,
        "div.gX_DSx2u_rsB8O6i"
    ).text

    duration = row.find_element(
        By.CSS_SELECTOR,
        "div.Na06TEk5cCR4FwBd"
    ).text

    # mở tab mới
    driver.execute_script("window.open(arguments[0])", track_url)

    driver.switch_to.window(driver.window_handles[-1])

    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR,'span[data-testid="release-date"]')
        )
    )

    year = driver.find_element(
        By.CSS_SELECTOR,
        'span[data-testid="release-date"]'
    ).text

    driver.close()

    driver.switch_to.window(driver.window_handles[0])

    data.append({
        "track_id":track_id,
        "artist_id":artist_id,
        "track_name":name,
        "year":year,
        "duration":duration,
        "image":image,
        "play_count":playcount,
        "url":track_url
    })

df = pd.DataFrame(data)

print(df)

df.to_csv("spotify.csv",index=False,encoding="utf-8-sig")

driver.quit()