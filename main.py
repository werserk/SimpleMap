import sys
import PyQt5.QtWidgets as QtWidgets
from MapRequest import get_map_image


class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Основные параметры
        self.map_size = 600  # Если слишком большой(маленький) размер каринки, то изменить здесь
        self.x = 37.621094
        self.y = 55.7536
        self.delta = 0.005  # Коэффицент отдаления

        # Инициализация окна
        self.initUI()

    def initUI(self):
        # Настройки окна
        self.width = self.map_size
        self.height = self.map_size - 60
        self.setGeometry(0, 0, self.width, self.height)
        self.setFixedSize(self.size())
        self.setStyleSheet('background: lightblue')
        self.setWindowTitle('Карты')

        # Рамка для картинки
        self.frame_for_picture = QtWidgets.QLabel(self)
        self.frame_for_picture.setGeometry(0, 0, self.width, self.height - 20)
        self.frame_for_picture.setStyleSheet('background: white')

        # Кнопка поиска
        self.btn_search = QtWidgets.QPushButton(self)
        self.btn_search.setGeometry(0, 0, self.width, 40)
        self.btn_search.setText('Найти!')
        self.btn_search.clicked.connect(self.search)

        # Рамка для отображения информации
        self.frame_settings_for_search = QtWidgets.QFrame(self)
        self.frame_settings_for_search.setGeometry(0, self.height - 20,
                                                   self.width, 20)
        # Информация о карте
        self.lbl_x = QtWidgets.QLabel(self)
        self.lbl_x.setGeometry(0, self.height - 20, 100, 20)
        self.lbl_y = QtWidgets.QLabel(self)
        self.lbl_y.setGeometry(100, self.height - 20, 100, 20)
        self.lbl_delta = QtWidgets.QLabel(self)
        self.lbl_delta.setGeometry(200, self.height - 20, 100, 20)

    def search(self):
        # Получаемся картинку
        pixmap = get_map_image(self.x, self.y, self.delta)
        resize_coef = min(self.frame_for_picture.width() / pixmap.width(),
                          self.frame_for_picture.height() / pixmap.height())
        pixmap = pixmap.scaled(int(pixmap.width() * resize_coef),
                               int(pixmap.height() * resize_coef))

        # Отображаем параметры
        self.lbl_x.setText(f'x: {round(self.x, 5)}')
        self.lbl_y.setText(f'y: {round(self.y, 5)}')
        self.lbl_delta.setText(f'delta: {round(self.delta, 5)}')

        # Отображаем картинку
        self.frame_for_picture.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainApp()
    ex.show()
    sys.exit(app.exec())
