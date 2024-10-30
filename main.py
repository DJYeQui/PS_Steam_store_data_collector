from GameIdList import GameIdList
from GamePage import game_info

# URL of the website you want to scrape
url = "https://store.playstation.com/en-tr/category/d0446d4b-dc9a-4f1e-86ec-651f099c9b29/1"  # sample url
b = GameIdList()
a = b.read_all_game_ids(url, 1, 2)

for game_id in a:
    general_url = "https://store.playstation.com/en-tr/concept/" + str(game_id)
    print(general_url)
    game_page = game_info(general_url)
