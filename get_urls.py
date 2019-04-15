from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
import re
import time
import csv
user_agent = {'User-agent': 'Mozilla/5.0'}

# Получаем html-код страницы http://altaysnab.ru/catalog/
def get_html(url):
    catalog_request = requests.get(url, user_agent)
    return catalog_request.text


# Получаем все ссылки на группы товаров в каталоге и добавляем их в массив
def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tools = soup.find_all('div', class_='catalog-section-child')
    tools_links = []
    for td in tools:
        a = td.find('a').get('href')
        link = 'http://altaysnab.ru' + a
        tools_links.append(link)
    return tools_links


# Получаем html всех страниц групп товаров(Бензотехника, Измерительный инструмент и.т.д.)
def get_catalog_html(link):
    item_groups = requests.get(link, user_agent)
    return item_groups.text


# Проходим по всем товарам в группе и собираем их названия. Возвращаем список с наименованиями товаров.
def get_item_title(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find('div', class_='catalog-item-table-view').find_all('div', class_='item-all-title')
    list_items = []
    for i in items:
        list_items.append(i.find('span').string)
    return list_items


# Проходим по всем товарам в группе и собираем их цены. Возвращаем список с ценами товаров.
def get_item_price(html):
    soup = BeautifulSoup(html, 'lxml')
    price = soup.find('div', class_='catalog-item-table-view').find_all('span', class_='catalog-item-price')
    list_price = []
    for i in price:
        list_price.append(i.get_text().strip().split('\t')[0])
    return list_price


# Формируем словарь из списков
def make_dict(item_name, item_price):
    price_items_dict = dict(zip(item_name, item_price))
    return price_items_dict


def write_csv(dict):
    with open('test.csv', 'w') as f:
        writer = csv.writer(f)
        for key in dict.keys():
            writer.writerow((
                key,
                dict[key]
            ))


# def main():
#     url = 'http://altaysnab.ru/catalog/'
#     all_links = get_all_links(get_html(url))
#     Тут погружаемся в пучину
#     item_name = []
#     item_price = []
#     for i in all_links:
#         item_name.append(get_item_title(get_catalog_html(i)))
#         item_price.append(get_item_price(get_catalog_html(i)))
#     items_dict = make_dict(item_name, item_price)
#     write_csv(items_dict)


url = 'http://altaysnab.ru/catalog/'
all_links = get_all_links(get_html(url))
print(all_links)
item_name = []
item_price = []
for i in all_links[0:1]:
    item_name.append(get_item_title(get_catalog_html(i)))
    item_price.append(get_item_price(get_catalog_html(i)))


for i in item_name:
    print(i)
# price_items_dict = dict(zip(item_name, item_price))
# print(price_items_dict)



# main()





# print(get_all_links(get_html('http://altaysnab.ru/catalog/')))