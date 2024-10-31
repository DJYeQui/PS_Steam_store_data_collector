import csv
from GameIdList import GameIdList
from GamePage import game_info


def write_game_info_to_csv(game_data, filename="146_page_to_160.csv"):
    # if there is not csv it will create else it will edit
    file_exists = False
    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            file_exists = True
    except FileNotFoundError:
        pass

    # for add mod "a"
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        # take headers from game_data keys
        fieldnames = game_data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        # if there is not write it again
        if not file_exists:
            writer.writeheader()

        # write csv file
        writer.writerow(game_data)

    print(f"Veri '{filename}' dosyasına başarıyla eklendi.")


# URL you want to scrape
url = "https://store.playstation.com/tr-tr/pages/browse/1"  # sample url
b = GameIdList()
page_game_id_list = b.read_all_game_ids_in_page(url, 1, 1, "?PS5=targetPlatforms")

for game_id in page_game_id_list:
    general_url = "https://store.playstation.com/en-tr/concept/" + str(game_id)
    write_game_info_to_csv(game_info(general_url))
