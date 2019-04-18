import csv
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool
import time

proxies = {
    'https': 'https://103.119.54.48:8080',
}

# Читаем ссылки из CSV файла
# сохраняем в переменную links
# срез [::2] для того,чтобы брать каждую вторую строку, т.к. вторая строка - пустой список и я понятия не имею, почему
# TO-DO: Починить запись в CSV


# def read_data():
#     with open('links.csv', 'r') as f:
#         reader = csv.reader(f)
#         data = [row for row in reader]
#         links = data[::2]
#     return links


def read_data():
    with open('links.txt', 'r') as f:
        reader = f.readlines()
        data = [row for row in reader]
        data = [line.rstrip() for line in data]
        links = data[:]
    return links


# Получаем HTML-код по ссылке


# def get_html(links):
#     for link in links:
#         r = requests.get(link[0])
#         return r.text


def get_html(links):
    r = requests.get(links, proxies=proxies)
    print(r.status_code)
    return r


# Получаем название товара


# def get_item_title(html):
#     soup = BeautifulSoup(html, 'lxml')
#     items = soup.find('div', class_='catalog-item-table-view').find_all('div', class_='item-all-title')
#     list_items = []
#     for i in items:
#         list_items.append(i.find('span').string)
#     return list_items


def get_item_title(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        items = soup.find('div', class_='catalog-item-table-view').find_all('div', class_='item-all-title')
    except AttributeError:
        print('Адмирал, похоже блядский Алтснаб спалил нас!')
        print("Не удалось спарсить:")
        items = []
    list_items = []
    for i in items:
        list_items.append(i.find('span').string)
    return list_items


#  Получаем цену товара


def get_item_price(html):
    soup = BeautifulSoup(html, 'lxml')
    price = soup.find('div', class_='catalog-item-table-view').find_all('span', class_='catalog-item-price')
    list_price = []
    for i in price:
        list_price.append(i.get_text().strip().split('\t')[0])
    return list_price

# Формируем словарь из описания товара и цены


def make_dict(item_name, item_price):
    price_items_dict = dict(zip(item_name, item_price))
    return price_items_dict

# Записываем словарь в CSV файл


def write_csv(dictionary):
    with open('items_prices.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        for key in dictionary.keys():
            writer.writerow((
                key,
                dictionary[key]
            ))


def make_all(links):
    html = get_html(links)
    # print(html)
    # time.sleep(2)
    if html.status_code == 404:
        item_title = ['не удалось спарсить, ошибка ' + str(html.status_code)]
        item_price = ['не удалось спарсить, ошибка ' + str(html.status_code)]
    else:
        item_title = get_item_title(html.text)
        item_price = get_item_price(html.text)
    print(item_title)
    # time.sleep(2)
    # item_price = get_item_price(html.text)
    print(item_price)
    # time.sleep(2)
    dictionary = make_dict(item_title, item_price)
    write_csv(dictionary)
    print('Done')


# def main():
#     links = [read_data()]
#     with Pool(40) as p:
#         p.map(make_all, links)
links = read_data()
for i in links:
    make_all(i)

# if __name__ == '__main__':
#     main()