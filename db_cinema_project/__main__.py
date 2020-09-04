import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

from db_cinema_project.db import utils
from db_cinema_project.ui import auth_form, \
    main_form, main  # Это наш конвертированный файл дизайна


class Table(QtWidgets.QWidget):
    def __init__(self, res):
        super().__init__()
        self.title = 'Таблица сторудников'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))

        for row_number, row_data in enumerate(res):
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,
                                         QtWidgets.QTableWidgetItem(str(data)))

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, db):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.print_db)
        self.db = db

    def print_db(self):
        res = self.db.get_all_stuff()
        self.table = Table(res)
        self.table.show()


class AuthApp(QtWidgets.QMainWindow, auth_form.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.authButton.clicked.connect(self.auth)
        self.dialog = QtWidgets.QErrorMessage()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Не удалось подключиться.")
        self.msg.setWindowTitle("Ошибка подключения")
        self.msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.ok)

        self.db = None

    def ok(self):
        self.msg.close()

    def auth(self):
        login = self.login.text()
        password = self.password.text()
        try:
            self.db = utils.DBCinema('localhost', login, password,
                                     'labs')
            self.close()
            self.Open = MainApp(self.db)
            self.Open.show()
        except RuntimeError:
            self.msg.show()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AuthApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
