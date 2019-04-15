from bs4 import BeautifulSoup
import requests
import re
import time
import csv
user_agent = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                            'Safari/537.36'})


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

url = 'http://altaysnab.ru/catalog/'
all_links = get_all_links(get_html(url))
list_items = []
list_price = []
for i in all_links:
    r = requests.get(i)

    soup = BeautifulSoup(r.text, 'lxml')

    items = soup.find('div', class_='catalog-item-table-view').find_all('div', class_='item-all-title')
    price = soup.find('div', class_='catalog-item-table-view').find_all('span', class_='catalog-item-price')
    for i in items:
        list_items.append(i.find('span').string)
    for i in price:
        list_price.append(i.get_text().strip().split('\t')[0])

price_items_dict = dict(zip(list_items, list_price))

for k, v in price_items_dict.items():
    print(k, v)


# with open('test.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for key in price_items_dict.keys():
#         writer.writerows(([key],
#             [price_items_dict[key]]
#         ))

with open('test.csv', 'w') as f:
    writer = csv.writer(f)
    for key, val in price_items_dict.items():
        writer.writerow([str(key), str(val)])

