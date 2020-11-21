import os

from PyQt5 import QtWidgets

from db_cinema_project.db import utils
from db_cinema_project.db.hashers import PBKDF2PasswordHasher
from db_cinema_project.db.utils import DBException
from db_cinema_project.ui import reg_form
from db_cinema_project.user_cabinet import LKApp


class RegApp(QtWidgets.QMainWindow, reg_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка регистрации")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.pushButton.clicked.connect(self.register)
        self.db = None
        self.id = None
        self.msg.buttonClicked.connect(self.ok)

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
        if not name:
            self.msg.setText("Введите ФИО.")
            self.msg.show()
        elif not email:
            self.msg.setText("Введите почту.")
            self.msg.show()
        elif not password:
            self.msg.setText("Введите пароль.")
            self.msg.show()
        else:
            self.db = utils.DBCinema(os.getenv('DB_HOST'), os.getenv('DB_USER'),
                                     os.getenv('DB_PASSWORD'),
                                     os.getenv('DB_DATABASE'))
            try:
                hasher = PBKDF2PasswordHasher()
                hash_ = hasher.encode(password, hasher.salt())
                uid = self.db.add_user(name, email, number, hash_)

                self.close()
                self.Open = LKApp(self.db, uid)
                self.Open.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()
