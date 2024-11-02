import csv 

def read_csv() -> list:
    file_name = 'psn_game_data.csv'

    data = [];
    with open(file_name, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row[1]) > 0:
                row[1] = row[1].split('\xa0TL')[0]
            if len(row[2]) > 0:
                row[2] = row[2].split('\xa0TL')[0]
            if len(row[3]) > 0:
                row[3] = row[3].split('\xa0TL')[0]
            if len(row[4]) > 0: 
                row[4] = row[4].split('\xa0TL')[0]
            data.append(row)
    
    print(data)
    return data;


def write_csv() -> None:
    file_name = 'fixed.csv'
    titles = ['name:', 'price:', 'discounted_price:', 'psn_price:', 'psn_old_price:', 'rating:', 'rating_count:', 'situation:', 'Collection Date:', 'Platform:', 'Release:', 'Genres:', 'Publisher:', 'Voice:', 'Screen Languages:', 'PS5 Voice:', 'PS5 Screen Languages:', 'PS4 Voice:', 'PS4 Screen Languages:', 'Link:']

    data = read_csv();
    with open(file_name, mode='w', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(titles)
        for row in data:
            csv_writer.writerow(row)
    print('CSV file has been written successfully')
    


if __name__ == '__main__':
    write_csv();