import requests
from bs4 import BeautifulSoup
import re

def collect_game_data_with_url(url: str, name: str = "empty"):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    game_data = {}

    # Oyun Adı
    if name == "empty":
        name_block = soup.find("div", id="appHubAppName", class_="apphub_AppName")
        game_data["Title"] = name_block.text.strip() if name_block else "Could not be taken from Steam"
    else:
        game_data["Title"] = name

    # Açıklama (Description)
    description_block = soup.find("div", class_="game_description_snippet")
    game_data["Description"] = description_block.text.strip() if description_block else "No description available"

    # Türler (Genres)
    tags_div = soup.find("div", class_="glance_tags popular_tags")
    if tags_div:
        genres = [tag.text.strip() for tag in tags_div.find_all("a", class_="app_tag")]
        game_data["Genre Labels"] = ", ".join(genres) if genres else "No genres available"

    # Çıkış Tarihi (Release Date)
    release_date_div = soup.find("div", class_="release_date")
    if release_date_div:
        release_date = release_date_div.find("div", class_="date")
        game_data["Release Date"] = release_date.text.strip() if release_date else "Unknown"

    # Geliştirici (Developers)
    developer_div = soup.find("div", id="developers_list")
    if developer_div:
        developers = [a.text.strip() for a in developer_div.find_all("a")]
        game_data["Developers"] = developers if developers else ["Unknown"]

    # Yayıncı (Publishers)
    publishers_div = soup.find_all("div", class_="summary column")
    publishers = []
    for div in publishers_div:
        if div.get("id") != "developers_list":
            publishers.extend([a.text.strip() for a in div.find_all("a")])
    game_data["Publishers"] = publishers if publishers else ["Unknown"]

    # Aylık İncelemeler (Recent Reviews)
    review_row_monthly = soup.find("div", class_="user_reviews_summary_row")
    if review_row_monthly:
        game_data["Review Status Monthly"] = review_row_monthly.find("span", class_="game_review_summary").text.strip()
        review_count_span = review_row_monthly.find("span", class_="responsive_hidden")
        game_data["Review Count Monthly"] = int(re.sub(r"[^\d]", "", review_count_span.text)) if review_count_span else -1
        review_desc_span = review_row_monthly.find("span", class_="nonresponsive_hidden responsive_reviewdesc")
        game_data["Review Description Monthly"] = review_desc_span.text.strip() if review_desc_span else "No description available"

    # Toplam İncelemeler (Total Reviews)
    review_row_total = soup.find("div", class_="user_reviews_summary_row", itemprop="aggregateRating")
    if review_row_total:
        game_data["Review Status Total"] = review_row_total.find("span", class_="game_review_summary").text.strip()
        review_count_span = review_row_total.find("span", class_="responsive_hidden")
        game_data["Review Count Total"] = int(re.sub(r"[^\d]", "", review_count_span.text)) if review_count_span else -1
        review_desc_span = review_row_total.find("span", class_="nonresponsive_hidden responsive_reviewdesc")
        game_data["Review Description Total"] = review_desc_span.text.strip() if review_desc_span else "No description available"

    # Fiyat (İndirimli ve Orijinal Fiyat)
    discount_block = soup.find("div", class_="discount_block game_purchase_discount")
    game_data["Original Price"] = "none"
    game_data["Discount Final Price"] = "none"

    if discount_block:
        # Orijinal fiyat (İndirim öncesi)
        original_price_div = discount_block.find("div", class_="discount_original_price")
        game_data["Original Price"] = original_price_div.text.strip() if original_price_div else "N/A"

        # İndirimli fiyat (Son fiyat)
        final_price_div = discount_block.find("div", class_="discount_final_price")
        game_data["Discounted Price"] = final_price_div.text.strip() if final_price_div else "N/A"

        # İndirim yüzdesi
        discount_pct_div = discount_block.find("div", class_="discount_pct")
        game_data["Discount Percentage"] = discount_pct_div.text.strip() if discount_pct_div else "N/A"
    else:
        # 2️⃣ **İndirim Yoksa Normal Fiyatı Çek**
        normal_price_div = soup.find("div", class_="game_purchase_price price")
        if normal_price_div:
            game_data["Original Price"] = normal_price_div.text.strip()  # Tek fiyat varsa orijinal fiyattır
            game_data["Discounted Price"] = "No discount"
            game_data["Discount Percentage"] = "No discount"

    # Yaş Derecelendirme (PEGI)
    rating_img = soup.find("div", class_="game_rating_icon")
    rating_number = "NONE"
    if rating_img:
        img_tag = rating_img.find("img")
        if img_tag and "src" in img_tag.attrs:
            rating_match = re.search(r"/(\d+)\.png", img_tag["src"])
            if rating_match:
                rating_number = rating_match.group(1)
    game_data["PEGI"] = rating_number if rating_number else "Not found"

    # Metacritic Puanı
    metacritic_score = soup.find("div", class_="score high")
    game_data["Metacritic Score"] = metacritic_score.text.strip() if metacritic_score else "No score available"

    # Desteklenen Diller (Languages)
    languages_block = soup.find("table", class_="game_language_options")
    languages = []
    if languages_block:
        rows = languages_block.find_all("td", class_="ellipsis")
        languages = [row.text.strip() for row in rows]
    game_data["Languages"] = languages if languages else ["Unknown"]

    return game_data

# a = collect_game_data_with_url("https://store.steampowered.com/app/2246340/Monster_Hunter_Wilds/")
# print(a)
#
# for game in a.keys():
#
#     print(game)
