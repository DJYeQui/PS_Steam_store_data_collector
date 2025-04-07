from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


def collect_link_from_steam_game_list(url: str) -> dict:
    # Tarayıcı seçenekleri
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Arka planda çalıştır
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # WebDriver başlat
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Steam Top Selling sayfasına git
    driver.get(url)
    time.sleep(5)

    # Oyun isimlerini ve bağlantılarını içeren öğeleri bul
    games = driver.find_elements(By.CSS_SELECTOR, "a._2C5PJOUH6RqyuBNEwaCE9X")
    game_name_with_links = {}
    for game in games[:10]:
        try:
            title = game.find_element(By.CSS_SELECTOR, "div._1n_4-zvf0n4aqGEksbgW9N").text  # game name
            link = game.get_attribute("href")
            print(f"{title}: {link}")
            game_name_with_links[title] = link
        except Exception as e:
            print("Veri çekme hatası:", e)

    driver.quit()
    return game_name_with_links
