import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import modification_of_links as modify

# **İstenmeyen Parametreler (Toplanmaması Gerekenler)**
EXCLUDED_KEYS = [
    "Store data followers",
    "Store data in top sellers",
    "Store data positive reviews",
    "Store data negative reviews",
    "Store data positive reviews percentage",
    "Twitch stats viewers right now",
    "Twitch stats 24-hour peak",
    "Twitch stats all-time peak",
    "Twitch stats "
]

# **Geri kalan toplanması gereken parametreler**
EXPECTED_KEYS = [
    "Owner estimations by VG Insights",
    "Owner estimations by Gamalytic",
    "Owner estimations by PlayTracker",
    "Owner estimations by SteamSpy"
]

def convert_to_number(value):
    """k veya M içeren değerleri sayıya çevirir."""
    if value.endswith("k"):
        return int(float(value.replace("k", "")) * 1000)
    elif value.endswith("M"):
        return int(float(value.replace("M", "")) * 1000000)
    try:
        return int(value)  # Eğer k veya M yoksa, direkt sayıya çevir
    except ValueError:
        return -1  # Eğer sayıya çevrilemiyorsa -1 döndür

def collect_steamDB_selling_data(game_data_list):
    options = uc.ChromeOptions()
    options.headless = False  # Tarayıcıyı görmek istersen False yap
    driver = uc.Chrome(options=options)

    try:
        for game_data in game_data_list:
            steamdb_url = modify.change_id_of_link_for_steamDB(game_data["link"])  # Her oyun için SteamDB linkini al
            game_data["steamdb_url"] = steamdb_url

            print(f"Veri çekiliyor: {steamdb_url}")
            driver.get(steamdb_url)

            # **Sayfanın tamamen yüklenmesini bekle**
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "row-app-charts"))
            )

            # Sayfanın içeriğini al ve BeautifulSoup ile işle
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # **Bölüm başlıklarını çek**
            sections = soup.find_all("div", class_="span4")

            extracted_data = {}  # Çekilen verileri burada saklayacağız

            for section in sections:
                section_title_tag = section.find("h3")
                if section_title_tag:
                    section_title = section_title_tag.text.strip()

                    # İçerikteki tüm <li> öğelerini al
                    for li in section.find_all("li"):
                        strong = li.find("strong")
                        if strong:
                            key_text = li.text.strip().replace(strong.text.strip(), "").strip()  # Örneğin "followers"
                            value_text = strong.text.strip().replace("~", "")  # Sayısal değeri al
                            key = f"{section_title} {key_text}"

                            # **Eğer bu key EXCLUDED_KEYS içinde varsa, atla**
                            if key in EXCLUDED_KEYS:
                                continue

                            # k ve M içeren verileri sayıya çevir
                            extracted_data[key] = convert_to_number(value_text)

            # **Eksik verileri `-1` ile doldur (sadece beklenenler)**
            for key in EXPECTED_KEYS:
                if key not in extracted_data:
                    extracted_data[key] = -1  # Eksikse -1 olarak ekle

            # Çekilen verileri game_data'ya ekle
            game_data.update(extracted_data)

    except Exception as e:
        print(f"Hata oluştu: {e}")

    finally:
        try:
            driver.quit()  # Tarayıcıyı düzgün şekilde kapat
        except OSError:
            print("Tarayıcı zaten kapalı.")

    return game_data_list

# Kullanım Örneği: Verilen game_data_list
game_data_list = [
    {"name": "Game 1", "link": "https://steamdb.info/app/1013320/charts/"},
    {"name": "Counter-Strike 2", "link": "https://steamdb.info/app/2198150/charts/"},
]

# # **Verileri çek**
# data_list = collect_steamDB_selling_data(game_data_list)
#
# # **Çekilen verileri yazdır**
# for game_data in data_list:
#     print(game_data)
