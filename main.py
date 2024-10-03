import requests
from tqdm import tqdm
import time
import json
class VK:


    def __init__(self, access_token, user_id, ya_disk_token, version='5.131'):

        self.token = access_token

        self.id = user_id

        self.yandex_disk_token = ya_disk_token

        self.version = version

        self.params = {'access_token': self.token, 'v': self.version}


    def users_info(self):

        url = 'https://api.vk.com/method/users.get'

        params = {'user_ids': self.id}

        response = requests.get(url, params={**self.params, **params})

        return response.json()

    def get_sizes_by_likes(self, url):
        params = {'access_token': self.token, 'owner_id': -1, 'album_id': 'wall', 'v': 5.199, 'extended': 1,
                  'photo_sizes': 1}
        response = requests.get(url, params={**params}).json()
       # print(response['response']['items'])

        map_likes = {}
        for i in range(len(response['response']['items'])):
            #print(response['response']['items'][i]['likes'])
            key_curr = response['response']['items'][i]['likes']['count']
            for j in range(len(response['response']['items'][i]['sizes'])):
                # print(response['response']['items'][i]['sizes'][j]['height'])
                # print(response['response']['items'][i]['sizes'][j]['width'])
                value_curr = [response['response']['items'][i]['sizes'][j]['height'],
                              response['response']['items'][i]['sizes'][j]['width'],
                              response['response']['items'][i]['sizes'][j]['url']]
            map_likes[key_curr] = value_curr
        return map_likes

    def filename_form(self, map_likes, num_likes, name):
        key = str(num_likes)+'.jpg'
        h, w = map_likes[num_likes][0], map_likes[num_likes][1]
        name[key] = [h,w]
        return name

    def get_top_n_elements(self, dictionary, n):
        sorted_dict = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        top_n_elements = dict(list(sorted_dict.items())[:n])
        return top_n_elements

    def json_note_form(self, filename, sizes ):             # filename -sizes map
        json_curr = {}
        json_curr['filename'] = filename
        json_curr['size'] = sizes

        json_object = json.dumps(json_curr, indent=4)

        # Writing to sample.json
        with open(filename[:-4]+".json", "w") as outfile:
            outfile.write(json_object)
        return json_curr

    def yandex_request(self, url, filename):
        for h in tqdm(range(1),
                      desc="Loading…"+filename,
                      ascii=False, ncols=75):

            headers = {
                'Authorization': self.yandex_disk_token
            }
            params = {
                'url': url,
                'path': 'folder/'+filename  # Путь, куда загрузить файл на Яндекс.Диске
            }

            response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                     headers=headers, params=params)
            time.sleep(0.1)

        print("Complete loading")


################### vk-class functions

token ='vk1.a.49tFuCEngbgiwCrx9xP35Bcagw9vE9qyobnlHnyijn0pQXGq0JB68worAnGhWBEpUxVKs3kxhfEHN4ABi2Th8Iw9Vkd8psdjA1ecns0QczH9NiuhU8he_oP5-MbF28qIiAhivKi3EFVS14wY41SJRvJ9540Vv2243V-2P26TYZ4KMQiwWTV95e-nz6OZu2zN'
user_id = 52368956
ya_disk_token ='y0_AgAAAAAUu06EAADLWwAAAAESS_xkAABmBMoZL7hG4KJsLrT_ZiTh9W1L_g'
vk = VK(token, user_id, ya_disk_token)          # объект класса vk
print(vk.users_info())
print('\n\n')

vk_photos_map = vk.get_sizes_by_likes('https://api.vk.com/method/photos.get')  #словарь размеров фотографий по лайкам
name={}                                                 # формирование названий файлов
for i in vk_photos_map.keys():
    vk.filename_form(vk_photos_map, i, name)

top_sizes = vk.get_top_n_elements(name, 5)                 # нахождение файлов с наибольшими размерами, сортировка
keys = top_sizes.keys()                                    #  название файлов - ключи
values = top_sizes.values()                                #  размеры файлов - значения

######## запись в json и в яндекс-диск #########

json_map ={}

for i in keys:
        print('\n',vk.json_note_form(i, top_sizes[i]))

        json_map=vk.json_note_form(i, top_sizes[i])

        url = vk_photos_map[int(i[:-4])][2]
        filename = i
        vk.yandex_request(url, filename)        # запись в яндекс диск

#######################################
