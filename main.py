import sys
from PyQt5 import Qt, QtWidgets, QtCore
from MapRequest import get_map_image

KEY_LEFT = 16777234
KEY_UP = 16777235
KEY_RIGHT = 16777236
KEY_DOWN = 16777237


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Основные параметры
        self.map_size = 600  # Если слишком большой(маленький) размер каринки, то изменить здесь
        self.x = 37.527256
        self.y = 55.723587
        self.z = 16
        self.map_type = 'map'

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

        # Изменение вида карты
        self.types_of_map = ['map', 'sat', 'sat,skl']

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

        # Отобазим картинку
        self.search()

    def search(self):
        # Получаемся картинку
        pixmap = get_map_image(self.x, self.y, self.z, self.map_type)
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

    def cmd_wheel_up(self):
        self.z += 1
        if self.z >= 17:
            self.z = 17

        # Отобразим картинку
        self.search()

    def cmd_wheel_down(self):
        self.z -= 1
        if self.z <= 0:
            self.z = 0

        # Отобразим картинку
        self.search()

    def cmd_key_left(self):
        self.x -= 1 / self.z
        self.search()

    def cmd_key_right(self):
        self.x += 1 / self.z
        self.search()

    def cmd_key_up(self):
        self.y += 1 / self.z
        self.search()

    def cmd_key_down(self):
        self.y -= 1 / self.z
        self.search()

    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            if e.key() == KEY_LEFT:
                self.cmd_key_left()
            if e.key() == KEY_RIGHT:
                self.cmd_key_right()
            if e.key() == KEY_UP:
                self.cmd_key_up()
            if e.key() == KEY_DOWN:
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
