import time
import requests
from bs4 import BeautifulSoup


def game_info(url: str) -> dict:
    # Send GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all article titles and links

        game_info = {}
        # TODO game title
        title_tag = soup.find('h1', {'data-qa': 'mfe-game-title#name'})
        if title_tag:
            game_info['name:'] = title_tag.text
        else:
            game_info['name:'] = None

        # TODO game current price
        price_tag = soup.find('span', {
            'data-qa': 'mfeCtaMain#offer0#finalPrice'})  # Adjust tag and class based on the website's structure
        if price_tag:
            game_info['price:'] = price_tag.text
        else:
            game_info['price:'] = None

        # TODO game old price
        old_price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer0#originalPrice'})
        if old_price_tag:
            game_info['discounted_price:'] = old_price_tag.text
        else:
            game_info['discounted_price:'] = None

        # TODO game PSN price
        psn_price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer1#finalPrice'})
        if psn_price_tag:
            game_info['psn_price:'] = psn_price_tag.text
        else:
            game_info['psn_price:'] = None

        # TODO game PSN old price
        psn_old_price_tag = soup.find('span', {'data-qa': 'mfeCtaMain#offer1#originalPrice'})
        if psn_old_price_tag:
            game_info['psn_old_price:'] = psn_old_price_tag.text
        else:
            game_info['psn_old_price:'] = None

        # TODO game rating
        rating_tag = soup.find('div', {'data-qa': 'mfe-game-title#average-rating'})
        if rating_tag:
            game_info['rating:'] = rating_tag.text
        else:
            game_info['rating:'] = None

        # TODO game PSN rating amount
        rating_count_tag = soup.find('div', {'data-qa': 'mfe-game-title#rating-count'})
        if rating_count_tag:
            game_info['rating_count:'] = rating_count_tag.text
        else:
            game_info['rating_count:'] = None

        # TODO situation of selling
        button_tag = soup.find('button', {'data-qa': 'mfeCtaMain#cta#action'})
        if button_tag:
            game_info['situation:'] = preorder_text = button_tag.find('span').get_text(strip=True)
        else:
            game_info['situation:'] = None

        # TODO game info date publisher platform genres
        keys = soup.find_all('dt')
        values = soup.find_all('dd')

        """collumn names"""
        game_info['Collecting_date:'] = time.strftime("%m/%d/%Y")
        game_info['Platform:'] = None
        game_info['Release:'] = None
        game_info['Genres:'] = None
        game_info['Publisher:'] = None
        game_info['Voice:'] = None
        game_info['Screen_languages:'] = None



        # Anahtar-değer çiftlerini bir sözlükte saklayın
        for key, value in zip(keys, values):
            key_text = key.get_text(strip=True)
            value_text = value.get_text(" ", strip=True)  # Boşlukları temizleyerek metni alır
            game_info[key_text] = value_text

        game_info['Link:'] = url

        # Sonuçları yazdır
        for k, v in game_info.items():
            print(f"{k} {v}")
        return game_info
    else:
        print("Failed to retrieve the page")
