import requests
from bs4 import BeautifulSoup
from ExceptionList import InvalidParameterError


class GameIdList(object):
    # TODO game_id_list function is returns game ids which are in page with int List
    @staticmethod
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

    # TODO read_all_game_ids is returns selected pages games ids with int list
    def read_all_game_ids_in_page(self, cut_url: str, starting_page: int, end_page: int) -> list:
        end_page_index = end_page + 1
        page_index = starting_page
        if page_index > end_page or page_index <= 0 or end_page_index <= 0: raise InvalidParameterError(
            "start_page must be"
            "lower than "
            "end_page "
            "also they must "
            "be greater then 0")
        all_game_ids = []
        try:
            # If there is a number part in url
            if isinstance(int(cut_url[cut_url.rfind("/") + 1:]), int):
                for page_index_reading in range(page_index, end_page_index):
                    print(f"games ids are collecting \n page number: {page_index_reading} \n")
                    page_24_game_list = self.game_id_list(cut_url[:-1] + str(page_index_reading))
                    all_game_ids.extend(page_24_game_list)
            return all_game_ids
        except ValueError:
            for page_index_reading in range(page_index, end_page_index):
                print(f"games ids are collecting \n page number: {page_index_reading} \n")
                page_24_game_list = self.game_id_list(cut_url + str(page_index_reading))
                all_game_ids.extend(page_24_game_list)
            return all_game_ids
        except InvalidParameterError:
            print("Invalid parameter value for start and end page index")
        except:
            print("Failed to retrieve the page check url")
