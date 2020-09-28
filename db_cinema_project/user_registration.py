import os

import pymysql
from PyQt5 import QtWidgets

from db_cinema_project.db import utils
from db_cinema_project.db.hashers import PBKDF2PasswordHasher
from db_cinema_project.ui import reg_form
from db_cinema_project.user_cabinet import LKApp


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
