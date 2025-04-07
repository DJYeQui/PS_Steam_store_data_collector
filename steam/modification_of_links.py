def change_id_of_link_for_steamDB(link):
    id_of_game = ""
    if "/app/" in link:
        try:
            game_id = link.split("/app/")[1].split("/")[0]
            id_of_game = game_id
            print(f"Oyun ID: {game_id}")
        except IndexError:
            print(f"Hatalı link formatı: {link}")
    else:
        print(f"Geçersiz format: {link}")
    return f"https://steamdb.info/app/{id_of_game}/charts/"
