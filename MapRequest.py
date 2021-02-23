import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray


def get_map_image(toponym_longtitude, toponym_lattitude, delta):
    delta = str(delta)
    toponym_longtitude = str(toponym_longtitude)
    toponym_lattitude = str(toponym_lattitude)

    # Параметры для получения картинки
    map_params = {
        'll': ','.join([toponym_longtitude, toponym_lattitude]),
        'spn': ','.join([delta, delta]),
        'l': 'map'
    }

    # Сервер
    map_api_server = 'http://static-maps.yandex.ru/1.x/'

    # Получение ответа от сервера
    response = requests.get(map_api_server, params=map_params)

    # Перевод ответа в картинку
    payload = QByteArray(response.content)
    pixmap = QPixmap()
    pixmap.loadFromData(payload, "PNG")

    return pixmap
