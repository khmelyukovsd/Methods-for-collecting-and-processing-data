# 1) Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# записывающую собранные вакансии в созданную БД

# Импорт библиотек
from pymongo import MongoClient
import pandas as pd
from pprint import pprint

# Подключение к БД
client = MongoClient('localhost',27017)
db = client['db_vacancies']

hh = db.hh
sj = db.sj

# Загрузка датафреймов
df_hh = pd.read_csv('df_vacancies_hh_python.csv')
df_sj = pd.read_csv('df_vacancies_sj_python.csv')

def DF_to_DB(df, collection):
    for i in range(df.shape[0]):
        vac = df.loc[i]
        dictionary = {
            'name': vac['name'],
            'link': vac["link"],
            'company': vac["company"],
            'salary_min': vac["salary_min"],
            'salary_max': vac['salary_max'],
            'currency': vac["currency"],
            'source': vac["source"]}
        collection.insert_one(dictionary)

DF_to_DB(df_hh, hh)
DF_to_DB(df_sj, sj)

# 2) Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введенной суммы

def search_by_salary(collection, limit):
    vacancies = collection.find({'$or': [{'salary_min': {'$gt': limit}}, {'salary_max': {'$gt': limit}}]})
    for vacancy in vacancies:
        pprint(vacancy)

search_by_salary(hh, 400000)
search_by_salary(sj, 300000)

# 3*) Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта

def insert_new_vacancy(new_vacancy, collection):
     if collection.find({'link': new_vacancy['link']}) == False:
        collection.insert_one(new_vacancy)

new_vacancy1 = {'name': 'Программист',
                'link': 'https://korolev.hh.ru/vacancy/36784645',
                'company': 'Alfa-bank',
                'salary_min': '2500',
                'salary_max': '3000',
                'currency': 'USD'}
insert_new_vacancy(new_vacancy1, hh)
