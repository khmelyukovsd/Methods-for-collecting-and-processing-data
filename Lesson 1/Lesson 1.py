""" Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json"""

import requests
import json

main_link = 'https://api.github.com/users/'
token = '36275840dc4c9584d82d2d193b0713edd1c517d7'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/81.0.4044.129 Safari/537.36',
          'Authorization': token}

user_name = input('Введите имя пользователя на GitHub: ')
rep = '/repos'

response = requests.get(main_link + user_name + rep, headers=header)

if response.ok:
    data = json.loads(response.text)
    repositories = []
    print(f'Репозитории пользователя {user_name}:')
    for repos in data:
        print('- ', repos['name'])
        repositories.append(repos['name'])
else:
    print(f'Произошла ошибка {response.status_code}')

with open(f'{user_name}_repositories.json', 'w') as f:
    json.dump(repositories, f)
