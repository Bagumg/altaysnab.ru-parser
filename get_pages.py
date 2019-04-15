from bs4 import BeautifulSoup
import requests
import re
import time
import csv



# user_agent = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
#                             'Safari/537.36'})
#
#
# r = requests.get('http://altaysnab.ru/catalog/dreli_akkumulyatornye_shurupoverty/')
#
# soup = BeautifulSoup(r.text, 'lxml')
#
# lis = soup.find('div', class_='pagination').find_all('a')
# link = []
# for i in lis:
#     a = i.get('href')
#     link.append('http://altaysnab.ru' + a)
#
# last_page = re.findall(r'=(\d+)', link[-2])
#
#
# final_link = []
# for i in range(1, int(last_page[0]) + 1):
#     final_link.append(f'http://altaysnab.ru/catalog/dreli_akkumulyatornye_shurupoverty/?PAGEN_1={i}')
#
# print(final_link)



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


# print(all_links)
req_pack = []
link = []
final_link = []


# Погружаемся в пучину ада. Всё глубже и глубже
for i in all_links:
    # print(i)
    time.sleep(0.3)
    r = requests.get(i)
    # print(r)
    soup = BeautifulSoup(r.text, 'lxml')
    try:
        lis = soup.find('div', class_='pagination').find_all('a')
    except:
        lis = i

    for li in lis:
        try:
            a = li.get('href')
            link.append('http://altaysnab.ru' + a)
        except:
            link.append(i)

    last_page = re.findall(r'=(\d+)', link[-2])

    try:
        for j in range(1, int(last_page[0]) + 1):
            final_link.append(f'{i}?PAGEN_1={j}')
    except:
        final_link.append(i)

    link = []

    print(final_link)

with open('links.csv', 'w') as f:
    writer = csv.writer(f)
    for link in final_link:
        writer.writerow([link])
# print(final_link)