import requests
from bs4 import BeautifulSoup as BS


class Cats:
    host = "https://lapkins.ru"

    def __init__(self, name):
        self.name = name

    def search_cat(breed):
        read = requests.get("https://lapkins.ru/cat/")
        html = BS(read.content, "html.parser")
        item = html("a", class_="poroda-element")
        for el in item:
            names = ["0"] * 5
            names[0] = el.find("img")["alt"]
            if "кошка" in names[0]:
                c = names[0].find("кошка")
                names[1] = names[0][: c - 1]
            d = names[0].find("короткошерстная")
            if d > 0:
                names[2] = names[0][: d - 1]
            e = names[0].find("длинношерстная")
            if e > 0:
                names[3] = names[0][: e - 1]
            f = names[0].find("вислоухая")
            if f > 0:
                names[4] = names[0][: f - 1]

            for i in range(5):
                if names[i] == breed:
                    result = el["href"]
                    result = result[5:]
                    answer = "https://lapkins.ru/cat/" + result
                    return answer
        return -1

    def give_info_cat(url):
        read = requests.get(url)
        html = BS(read.content, "html.parser")

        # Краткая информация о породе кота/кошки
        first_arr = []
        item_1 = html.find(class_="info")("li")
        for el in item_1:
            first_arr.append(el.text)

        # Основные моменты кота/кошки
        second_arr = []
        item_2 = html.find(class_="info-lapa")("li")
        k = 0
        for el in item_2:
            second_arr.append(el.text)
            k += 1
            if k > 3:
                break
        return first_arr, second_arr

    def give_photo_cat(url):
        read = requests.get(url)
        html = BS(read.content, "html.parser")

        # Находим и вытаскиваем фото
        item = html.find(class_="start-img").find("img")["src"]
        host = "https://lapkins.ru"
        return host + item
