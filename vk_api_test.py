import vk  # Импортируем модуль vk

vk_token = '9dfa07419dfa07419dfa0741cd9d8619c999dfa9dfa0741ffae5478875654c94509d144 '

def get_members(groupid):  # Функция формирования базы участников сообщества в виде списка
    first = vk_api.groups.getMembers(group_id=groupid, v=5.131)  # Первое выполнение метода дает первую 1000 подписчиков
    print(first)
    return first


def get_posts(owner_id, count, offset):  # Функция формирования базы участников сообщества в виде списка
    mas = vk_api.wall.get(owner_id=owner_id, v=5.92, count=count, offset=offset)
    for i in range(count):
        if "#мастерклассыдлядетей" in mas['items'][i]['text']:
            print(mas['items'][i]['text'])
    return mas


if __name__ == "__main__":
    session = vk.Session(access_token=vk_token)  # Авторизация
    vk_api = vk.API(session)
    group_id = "-quantorium_krasnodar"
    owner_id = "-166263833"

    #get_members(group_id)
    get_posts(owner_id, 10, 0)
