import requests
from bs4 import BeautifulSoup


def game_info(url:str):
    # Send GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all article titles and links

        title_tag = soup.find('h1', {'data-qa': 'mfe-game-title#name'})
        if title_tag: print(title_tag.text)

        price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer0#finalPrice'})  # Adjust tag and class based on the website's structure
        if price_tag: print(f"normal price {price_tag.text}")

        old_price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer0#originalPrice'})
        if old_price_tag: print(f"discounted price {old_price_tag.text}")

        psn_price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer1#finalPrice'})
        if psn_price_tag: print(f"psn price {psn_price_tag.text}")

        # Orijinal fiyatı bulma
        psn_old_price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer1#originalPrice'})
        if psn_old_price_tag: print(f"psn old price {psn_old_price_tag.text}")

        rating_tag = soup.find('div', {'data-qa': 'mfe-game-title#average-rating'})
        if rating_tag: print(f"rating {rating_tag.text}")

        rating_count_tag = soup.find('div', {'data-qa': 'mfe-game-title#rating-count'})
        if rating_count_tag: print(f"rating count {rating_count_tag.text}")

        # Tüm <dt> ve <dd> etiketlerini bul
        keys = soup.find_all('dt')
        values = soup.find_all('dd')

        # Anahtar-değer çiftlerini bir sözlükte saklayın
        game_info = {}
        for key, value in zip(keys, values):
            key_text = key.get_text(strip=True)
            value_text = value.get_text(" ", strip=True)  # Boşlukları temizleyerek metni alır
            game_info[key_text] = value_text

        # Sonuçları yazdır
        for k, v in game_info.items():
            print(f"{k} {v}")
    else:
        print("Failed to retrieve the page")
