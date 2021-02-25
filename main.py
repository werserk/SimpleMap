import sys
from PyQt5 import Qt, QtWidgets, QtCore
from MapRequest import *

KEY_LEFT = 65, 16777234, 1060
KEY_UP = 87, 16777235, 1062
KEY_RIGHT = 68, 16777236, 1042
KEY_DOWN = 83, 16777237, 1067


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Основные параметры
        self.map_size = 600  # Если слишком большой(маленький) размер каринки, то изменить здесь
        self.x = 37.621094
        self.y = 55.7536
        self.coords_for_dota = self.x, self.y
        self.z = 16
        self.map_type = 'map'
        self.ind = 0
        self.toponym = 'Красная площадь'
        self.map_types = ['map', 'sat', 'sat,skl']

        # Инициализация окна
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.width = self.map_size
        self.height = self.map_size - 60
        self.setGeometry(0, 0, self.width, self.height)
        self.setFixedSize(self.size())
        self.setStyleSheet('background: lightgray')
        self.setWindowTitle('Карты')

        # Поиск объекта на карте
        self.edt_find_toponym = QtWidgets.QLineEdit(self)
        self.edt_find_toponym.setText(self.toponym)
        self.edt_find_toponym.setGeometry(0, 0, 450, 30)
        self.edt_find_toponym.setStyleSheet('background: white')

        self.btn_find_toponym = QtWidgets.QPushButton(self)
        self.btn_find_toponym.setText('Найти!')
        self.btn_find_toponym.setGeometry(450, 0, 70, 30)
        self.btn_find_toponym.clicked.connect(self.switch_toponym)

        # Изменение вида карты
        self.btn_box_map_types = QtWidgets.QPushButton(self)
        self.btn_box_map_types.setText('Тип')
        self.btn_box_map_types.setGeometry(self.width - 80, 0, 80, 30)
        self.btn_box_map_types.clicked.connect(self.switch_map_type)

        # Рамка для картинки
        self.frame_for_picture = QtWidgets.QLabel(self)
        self.frame_for_picture.setGeometry(0, 30, self.width, self.height - 20 - 30)
        self.frame_for_picture.setStyleSheet('background: white')

        # Рамка для отображения информации
        self.frame_settings_for_search = QtWidgets.QFrame(self)
        self.frame_settings_for_search.setGeometry(0, self.height - 20,
                                                   self.width, 20)
        # Информация о карте
        self.lbl_x = QtWidgets.QLabel(self.frame_settings_for_search)
        self.lbl_x.setGeometry(0, 0, 100, 20)
        self.lbl_y = QtWidgets.QLabel(self.frame_settings_for_search)
        self.lbl_y.setGeometry(100, 0, 100, 20)
        self.lbl_z = QtWidgets.QLabel(self.frame_settings_for_search)
        self.lbl_z.setGeometry(200, 0, 100, 20)

    def search(self):
        # Получаемся картинку
        pixmap = get_map_image((self.x, self.y), self.z, self.map_type, self.coords_for_dota)
        resize_coef = min(self.frame_for_picture.width() / pixmap.width(),
                          self.frame_for_picture.height() / pixmap.height())
        pixmap = pixmap.scaled(int(pixmap.width() * resize_coef),
                               int(pixmap.height() * resize_coef))

        # Отображаем параметры
        self.lbl_x.setText(f'x: {round(self.x, 5)}')
        self.lbl_y.setText(f'y: {round(self.y, 5)}')
        self.lbl_z.setText(f'size_coef: {round(self.z / 17, 5)}')

        # Отображаем картинку
        self.frame_for_picture.setPixmap(pixmap)

    def switch_map_type(self):
        # Переключаем на следующую карту
        self.ind = (self.ind + 1) % 3
        self.map_type = self.map_types[self.ind]
        self.search()

    def switch_toponym(self):
        self.toponym = self.edt_find_toponym.text()
        response = get_map_coords(self.toponym)
        if isinstance(response, str):
            QtWidgets.QMessageBox.question(self, response)
        else:
            self.x, self.y = response
            self.coords_for_dota = response
        self.search()

    def cmd_wheel_up(self):
        self.z += 1
        if self.z >= 17:
            self.z = 17
        self.search()

    def cmd_wheel_down(self):
        self.z -= 1
        if self.z <= 0:
            self.z = 0
        self.search()

    def cmd_key_left(self):
        self.x -= self.z ** (-2)
        self.search()

    def cmd_key_right(self):
        self.x += self.z ** (-2)
        self.search()

    def cmd_key_up(self):
        self.y += self.z ** (-2.4)
        self.search()

    def cmd_key_down(self):
        self.y -= self.z ** (-2.4)
        self.search()

    def keyPressEvent(self, e):
        print(e.key())
        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() in KEY_LEFT:
                self.cmd_key_left()
            if e.key() in KEY_RIGHT:
                self.cmd_key_right()
            if e.key() in KEY_UP:
                self.cmd_key_up()
            if e.key() in KEY_DOWN:
                self.cmd_key_down()

    def wheelEvent(self, e):
        # Прокрутка колёсика мыши
        if e.angleDelta().y() > 0:
            self.cmd_wheel_up()
        elif e.angleDelta().y() < 0:
            self.cmd_wheel_down()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec())
