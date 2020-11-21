import os

from PyQt5 import QtWidgets

from db_cinema_project.db import utils
from db_cinema_project.db.hashers import PBKDF2PasswordHasher
from db_cinema_project.ui import enter_form
from db_cinema_project.user_cabinet import LKApp
from db_cinema_project.user_registration import RegApp


class EnterApp(QtWidgets.QMainWindow, enter_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка входа")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
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
            self.db = utils.DBCinema(os.getenv('DB_HOST'), 'user0',
                                     '',
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
