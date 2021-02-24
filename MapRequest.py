import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray


def get_map_image(coords, z, map_type, coords_for_dota):
    z = str(z)
    coords_for_dota = ','.join((str(coords_for_dota[0]),
                                str(coords_for_dota[1])))
    coords = ','.join((str(coords[0]),
                       str(coords[1])))

    # Параметры для получения картинки
    map_params = {
        'll': coords,
        # 'pt': coords_for_dota + ',pm2am',
        'l': map_type,
        'z': z
    }

    # Сервер
    map_api_server = 'http://static-maps.yandex.ru/1.x/'

    # Получение ответа от сервера
    response = requests.get(map_api_server, params=map_params)

    # Перевод ответа в картинку
    payload = QByteArray(response.content)
    pixmap = QPixmap()
    if map_type != 'map':
        pixmap.loadFromData(payload, "JPG")
    else:
        pixmap.loadFromData(payload, "PNG")

    return pixmap
