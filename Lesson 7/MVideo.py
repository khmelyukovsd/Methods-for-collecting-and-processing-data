# Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
import json
import time
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


chrome_options = Options()
#chrome_options.add_argument('start-maximized')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome('/home/sergey/PycharmProjects/test/Lesson7/chromedriver', options=chrome_options)
driver.get('https://www.mvideo.ru/')
time.sleep(5)
assert "М.Видео" in driver.title
hits = driver.find_elements_by_xpath('//div[@class="gallery-layout"]')
actions = ActionChains(driver)
actions.move_to_element(hits[2])
actions.perform()

while True:
    try:
        button = driver.find_element_by_class_name('next-btn sel-hits-button-next')
    except:
        break
    actions.move_to_element(button).click().perform()

goods = driver.find_elements_by_xpath("//li[@class='gallery-list-item height-ready']//a[@data-product-info]")
print(1)
products = []
for good in goods:
    try:
        product = json.loads(good.get_attribute('data-product-info'))
        print(product)
        products.append(product)
    except:
        print('Парсинг окончен')

client = MongoClient('localhost', 27017)
db = client['products']
mvideo = db.mvideo

mvideo.insert_many(products)
driver.quit()
