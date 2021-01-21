import requests
import json


def get_info_all_photos(user_id):
    token_vk = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'
    response = requests.get('https://api.vk.com/method/photos.get',
        params={
            'user_id': user_id,
            'access_token': token_vk,
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'v': '5.126'
           })
    info_all_photo = response.json()['response']['items']
    return info_all_photo

def get_url_photos (info_all_photo):
    dict_photo = {}
    list_likes = []
    for info_photo in info_all_photo:
        likes: str = info_photo['likes']['count']
        date_photo: str = info_photo['date']
        name_photo = f'{likes}_{date_photo}.jpg'
        list_likes.append(name_photo)
        types_photo = info_photo['sizes']
        height_list = []
        for type_photo in types_photo:
            height_list.append(type_photo['height'])
            if type_photo['height'] == max(height_list):
                dict_photo[name_photo] = type_photo['url']
    return dict_photo

def get_type_photos (info_all_photo):
    dict_type = {}
    list_likes = []
    for info_photo in info_all_photo:
        likes: str = info_photo['likes']['count']
        date_photo: str = info_photo['date']
        name_photo = f'{likes}_{date_photo}.jpg'
        list_likes.append(name_photo)
        types_photo = info_photo['sizes']
        height_list = []
        for type_photo in types_photo:
            height_list.append(type_photo['height'])
            if type_photo['height'] == max(height_list):
                dict_type[name_photo] = type_photo['type']
    return dict_type

def get_json_photos(dict_type):
    json_file = []
    for key, value in dict_type.items():
        json_dict = {}
        json_dict["file_name"] = key
        json_dict["size"] = value
        json_file.append(json_dict)
    return json_file

def save_json(json_file):
    with open('json_file.json', 'w', encoding='utf8') as f:
        json.dump(json_file, f)
    return "json_file создан,"

def upload(token_yandex, dict_photo):
    resp1 = requests.put(
        "https://cloud-api.yandex.net/v1/disk/resources",
        params={"path": "Foto_VK_Profile"},
        headers={"Authorization": "OAuth" + " " + token_yandex}
    )
    resp1.raise_for_status()

    for k, v in dict_photo.items():
        path = "Foto_VK_Profile/" + k
        resp1 = requests.post(
            "https://cloud-api.yandex.net/v1/disk/resources/upload",
            params={"url": v, "path": path},
            headers={"Authorization": "OAuth" + " " + token_yandex}
        )
        resp1.raise_for_status()
    return 'Фотографии успешно загружены'


def main():
    user_id = input('Введите ваш ID VK: ')
    token_yandex = input('Введите ваш токен с Полигона Яндекс.Диска: ')
    add_yandex = (upload(token_yandex, (get_url_photos(get_info_all_photos(user_id)))))
    make_json = (save_json(get_json_photos(get_type_photos(get_info_all_photos(user_id)))))
    print(make_json, add_yandex)

main()
