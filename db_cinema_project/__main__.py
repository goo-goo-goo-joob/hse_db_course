import os

import pymysql
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets

from db_cinema_project.db import utils
from db_cinema_project.db.hashers import PBKDF2PasswordHasher
from db_cinema_project.ui import auth_form, \
    main, first_form, reg_form, enter_form, \
    lk_form  # Это наш конвертированный файл дизайна


class Table(QtWidgets.QWidget):
    def __init__(self, res):
        super().__init__()
        self.title = 'Таблица'
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


class LKApp(QtWidgets.QMainWindow, lk_form.Ui_MainWindow):
    def __init__(self, db, uid):
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.db = db
        self.id = uid
        self.name = self.db.get_user_name_by_id(uid)
        self.label.setText(f'Приветствуем Вас, {self.name}')
        self.pushButton.clicked.connect(self.print_db)

    def print_db(self):
        res = self.db.get_all_user_numbers()
        self.table = Table(res)
        self.table.show()


class EnterApp(QtWidgets.QMainWindow, enter_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка входа")
        self.msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.ok)
        self.pushButton.clicked.connect(self.enter)
        self.pushButton_2.clicked.connect(self.register)

    def ok(self):
        self.msg.close()

    def register(self):
        self.close()
        self.Open = RegApp()
        self.Open.show()

    def enter(self):
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()
        email = email if email else None
        password = password if password else None
        if not email:
            self.msg.setText("Введите почту.")
            self.msg.show()
        elif not password:
            self.msg.setText("Введите пароль.")
            self.msg.show()
        else:
            self.db = utils.DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'),
                                     os.getenv('DB_PASSWORD'),
                                     os.getenv('DB_DATABASE'))
            res = self.db.check_for_email(email)
            hasher = PBKDF2PasswordHasher()
            if not res[0]:
                self.msg.setText("Данный пользователь не зарегистрирован.")
                self.msg.show()
            elif not hasher.verify(password, res[1][1]):
                self.msg.setText("Пароль неверный.")
                self.msg.show()
            else:
                self.close()
                self.Open = LKApp(self.db, res[1][0])
                self.Open.show()


class RegApp(QtWidgets.QMainWindow, reg_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка регистрации")
        self.msg.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        self.msg.buttonClicked.connect(self.ok)
        self.pushButton.clicked.connect(self.register)
        self.db = None
        self.id = None

    def ok(self):
        self.msg.close()

    def register(self):
        name = self.name.text()
        email = self.email.text()
        number = self.number.text()
        password = self.password.text()
        name = name if name else None
        email = email if email else None
        number = number if number else None
        password = password if password else None
        self.db = utils.DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'),
                                 os.getenv('DB_PASSWORD'),
                                 os.getenv('DB_DATABASE'))
        try:
            hasher = PBKDF2PasswordHasher()
            hash = hasher.encode(password, hasher.salt())
            uid = self.db.add_user(name, email, number, hash)

            self.close()
            self.Open = LKApp(self.db, uid)
            self.Open.show()
        except AssertionError:
            self.msg.setText("Введите пароль.")
            self.msg.show()
        except pymysql.IntegrityError as error:
            code, message = error.args
            if code == 1048:
                self.msg.setText("Заполните обязательные поля.")
            elif code == 1062 and message[-6:] == 'почта\'':
                self.msg.setText("Пользователь с указанной почтой уже существует.")
            elif code == 1062 and message[-8:] == 'телефон\'':
                self.msg.setText(
                    "Пользователь с указанным номером телефона уже существует.")
            else:
                self.msg.setText("Не удалось зарегистрироваться.")
            self.msg.show()
        except pymysql.OperationalError as error:
            _, message = error.args
            self.msg.setText(message)
            self.msg.show()
        except pymysql.DataError as error:
            _, message = error.args
            if message[26:33] == 'телефон':
                self.msg.setText(
                    "Слишком длинный номер телефона. Введите его в соответствии с форматом +7xxxxxxxxxx.")
            else:
                self.msg.setText("Слишком длинные параметры ввода.")
            self.msg.show()
        except Exception:
            self.msg.setText("Не удалось зарегистрироваться.")
            self.msg.show()


class FirstApp(QtWidgets.QMainWindow, first_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_auth.clicked.connect(self.open_auth)
        self.btn_reg.clicked.connect(self.open_reg)
        self.btn_enter.clicked.connect(self.open_enter)

    def open_enter(self):
        self.close()
        self.Open = EnterApp()
        self.Open.show()

    def open_reg(self):
        self.close()
        self.Open = RegApp()
        self.Open.show()

    def open_auth(self):
        self.close()
        self.Open = AuthApp()
        self.Open.show()


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, db):
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
        except:  ## runtime_error???
            self.msg.show()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = FirstApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
