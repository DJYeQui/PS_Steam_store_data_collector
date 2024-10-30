import requests
from bs4 import BeautifulSoup


def game_id_list(url: str) -> list:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all article titles and links
        all_game_content_on_page = soup.find_all('a', {
            'data-telemetry-meta': True})  # Adjust tag and class based on the website's structure
        game_id_list = []

        # Loop through each article and print the title and link
        for game_content in all_game_content_on_page:
            if game_content:
                cut_game_data = game_content['data-telemetry-meta'].split(",")
                game_id_list.append(int(cut_game_data[0].split(":")[1].replace('"', "")))
            else:
                print("Data Telemetry Meta bulunamadı.")
        return game_id_list
    else:
        print("Failed to retrieve the page")


def read_all_game_ids(url:str, starting_page:int, end_page:int) -> list:
    end_page_index = end_page
    cut_url = "https://store.playstation.com/en-tr/category/d0446d4b-dc9a-4f1e-86ec-651f099c9b29/1"
    page_index = starting_page
    if page_index > end_page: raise InvalidParameterError
    all_game_ids = []
    try:
        if (isinstance(int(cut_url[cut_url.rfind("/") + 1:]), int)):
            for page_index in range(end_page_index):
                asd = game_id_list(cut_url[:-1] + str(page_index))
                all_game_ids.extend(asd)
                print(all_game_ids)
    except ValueError:
        for page_index in range(end_page_index):
            asd = game_id_list(cut_url + str(page_index))
            all_game_ids.extend(asd)
            print(all_game_ids)
    except:
        print("Failed to retrieve the page check url")

read_all_game_ids()
