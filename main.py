from GameIdList import GameIdList

# URL of the website you want to scrape
url = "https://store.playstation.com/en-tr/category/d0446d4b-dc9a-4f1e-86ec-651f099c9b29/1"  # sample url
b = GameIdList()
a = b.read_all_game_ids(url, 1, 20)

if 10010353 in a:
    print("True")
