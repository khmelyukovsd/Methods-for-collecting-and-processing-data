# 1) Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex.news
#    Для парсинга использовать xpath. Структура данных должна содержать:
#       * название источника,
#       * наименование новости,
#       * ссылку на новость,
#       * дата публикации
# 2) Сложить все новости в БД

from lxml import html
from pprint import pprint
import requests
import datetime
from pymongo import MongoClient

now = datetime.datetime.now().date()
news = []

#_______________________________________________________________________________________________________________________
# Парсинг yandex.news
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
main_link_Y = 'https://yandex.ru/news/'
response_Y = requests.get(main_link_Y, headers = header)
dom_Y = html.fromstring(response_Y.text)

dates_Y = dom_Y.xpath("//div[@aria-label='Главное']//div[@class='story__date']/text()")
name_Y = dom_Y.xpath("//div[@aria-label='Главное']//a[contains(@class,'link_theme_black')]/text()")
link_Y = dom_Y.xpath("//div[@aria-label='Главное']//h2[contains(@class,'story__title')]//@href")

for i in range(5):
    data = {}
    data['date'] = dates_Y[i][-5:] + ' ' + str(now)
    data['source'] = dates_Y[i][:-6]
    data['text'] = name_Y[i]
    data['link'] = main_link_Y[:-6] + link_Y[i]
    news.append(data)

#_______________________________________________________________________________________________________________________
# Парсинг lenta.ru
main_link_L = 'https://lenta.ru'
response_L = requests.get(main_link_L, headers = header)
dom_L = html.fromstring(response_L.text)

dates_L = dom_L.xpath("//section[contains(@class, 'main')]//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/time/@datetime")
name_L = dom_L.xpath("//section[contains(@class, 'main')]//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/text()")
link_L = dom_L.xpath("//section[contains(@class, 'main')]//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/@href")

# Первая новость из 10 имеет другие атрибуты и классы. Не нашел к чему прицепиться, поэтому только 9 новостей в цикле
for i in range(9):
    data = {}
    data['date'] = dates_L[i]
    data['source'] = main_link_L[8:]
    data['text'] = name_L[i].replace("\xa0",' ')
    data['link'] = main_link_L + link_L[i]
    news.append(data)

#_______________________________________________________________________________________________________________________
# Парсинг news.mail.ru
# main_link_M = 'https://news.mail.ru'
# response_M = requests.get(main_link_M, headers = header)
# dom_M = html.fromstring(response_M.text)
#
# dates_L = dom_L.xpath("//section[contains(@class, 'main')]//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/time/@datetime")
# name_L = dom_L.xpath("//section[contains(@class, 'main')]//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/text()")
# link_L = dom_L.xpath("//section[contains(@class, 'main')]//div[contains(@class, 'span4')]/div[contains(@class, 'item')]/a/@href")
#
# //div[contains(@class,'daynews__item')]

#_______________________________________________________________________________________________________________________
# Добавление данных в БД
client = MongoClient('localhost',27017)
db = client['NEWS']
news_collection = db.news
news_collection.insert_many(news)

#pprint(reviews)
