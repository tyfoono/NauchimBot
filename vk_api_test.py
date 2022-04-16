
import vk  # Импортируем модуль vk
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

vk_token = '9dfa07419dfa07419dfa0741cd9d8619c999dfa9dfa0741ffae5478875654c94509d144'

def get_posts(owner_id, count, offset):  # Функция формирования базы участников сообщества в виде списка
    mas = vk_api.wall.get(owner_id=owner_id, v=5.92, count=count, offset=offset)
    for i in range(count):
        if "#ITfest_2022" in mas['items'][i]['text']:
            print(mas['items'][i]['text'].encode('utf8').decode('utf8', 'ignore'))
    return mas


if __name__ == '__main__':
    session = vk.Session(access_token=vk_token)  # Авторизация
    vk_api = vk.API(session)
    group_id = 'itfest2022'
    owner_id = '-210985709'

    get_posts(owner_id, 1, 0)
