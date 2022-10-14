import requests
from bs4 import BeautifulSoup as BS
import csv
    

'''отправляем запрос на сайт'''
def get_html(url):
    response = requests.get(url)
    # print(response)
    return response.text

'''переводим в формат lxml'''
def get_soup(html):
    soup = BS(html, 'lxml')
    return soup

'''получаем название, описание, цену и картинку'''
def get_data(soup):
    catalog = soup.find('div', class_ = 'search-results-table')
    cars = catalog.find_all('div', class_ = 'list-item list-label')
    for car in cars:
        try:
            title = car.find('h2', class_ = 'name').text.strip()
        except:
            title = 'Нет названия'
        try:
            price = car.find('div', class_ = 'block price').find('strong').text.strip()
        except:
            price = 'Договорная'
        try:
            img = car.find('img', class_ = 'lazy-image').get('data-src')
        except:
            img = 'Нет фото'
        try:
            discription = car.find('div', class_ = 'block info-wrapper item-info-wrapper').text.split()
            discription_ = ','.join(discription)
            discription_ready = discription_.replace(',,', ',')
        except:
            discription = 'Нет описания'
        # print(discription_)
        write_csv({
            'title': title,
            'discription_ready':discription_ready,
            'img': img,
            'price': price
        })

'''Переводим в формат csv'''
def write_csv(data):
    with open('car.csv', 'a') as file:
        names = ['title', 'discription_ready', 'price' , 'img']
        write = csv.DictWriter(file, delimiter=',', fieldnames=names)
        write.writerow(data)

'''запуск программы'''
def main():
    try:
        for i in range(1, 100):
            BASE_URL = f'https://www.mashina.kg/search/all/?page={i}'
            html = get_html(BASE_URL)
            soup = get_soup(html)
            get_data(soup)
            print(f'Вы спарсили {i} страницу')
    except AttributeError:
        print('Эта была последняя страница')
    except KeyboardInterrupt:
        print('Принудительное завершение процесса')

if __name__== '__main__':
    main()
