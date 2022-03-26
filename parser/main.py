import requests
from bs4 import BeautifulSoup
import csv
CSV = 'mortgage.csv'
HOST = 'https://moskva.bankiros.u/'
URL = 'https://moskva.bankiros.ru/mortgage/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='row cr-row credits_row credits_row--for-mortgage')
    mortgage = []
    for item in items:
        mortgage.append({
            'title': item.find('div', class_= 'col-sm-3 col-xs-12 bank').get_text(),
            'link_bank': item.find('div', class_='col-sm-12').find('a').get('href'),
            'percent': item.find('span', class_='xxx-g-link xxx-accent-text').get_text(),
            'name_credit': item.find('div', class_='col-sm-12').get_text(),
            'image_bank': item.find('div', class_='col-sm-3 col-xs-12 bank').find('a').find('img').get('data-url-img')
        })
    return mortgage


def save_content(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название банка', 'Ипотечная программа на сайте банка', 'Процент', "Название ипотечной программы", "Лейбл банка"])
        for item in items:
            writer.writerow([item['title'], item['link_bank'], item['percent'], item['name_credit'], item['image_bank']])


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        items = get_content(html.content)
        save_content(items, CSV)
        print('Данные успешно записаны.')
    else:
        print(f'Ошибка {html.status_code}!')


parser()
