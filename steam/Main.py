import csv
import os

import game_link_list_collector as glc
import collect_game_data_from_link as collect
import modification_of_links as modification
import steamDB as db


def write_game_info_to_csv(game_final_data, filename="one_game.csv"):
    if not game_final_data:
        print("Hata: game_final_data boş!")
        return

    file_exists = os.path.isfile(filename)  # Dosyanın var olup olmadığını kontrol et
    fieldnames = game_final_data[0].keys()  # İlk elemandan anahtarları al

    with open(filename, mode="a", newline="", encoding="utf-8") as file:  # Append mode
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:  # Eğer dosya yoksa başlıkları yaz
            writer.writeheader()

        for row in game_final_data:
            writer.writerow(row)  # Her satırı ekle

    print(f"Veriler başarıyla {filename} dosyasına eklendi.")


def collect_many_games():
    link_list = glc.collect_link_from_steam_game_list("https://store.steampowered.com/charts/topselling/TR")
    game_data_list = []
    for name, link in link_list.items():
        game_data = collect.collect_game_data_with_url(link, name)
        game_data["link"] = link
        game_data_list.append(game_data)

    game_final_data = db.collect_steamDB_selling_data(game_data_list)
    write_game_info_to_csv(game_final_data)
    print("----------------------------------")


def collect_one_games(link: str):
    game_data_list = []
    game_data = collect.collect_game_data_with_url(link)
    game_data["link"] = link
    game_data_list.append(game_data)
    print(game_data)
    game_final_data = db.collect_steamDB_selling_data(game_data_list)
    write_game_info_to_csv(game_final_data)
    print(game_data)


#collect_one_games("https://store.steampowered.com/app/1766060/HumanitZ/")
