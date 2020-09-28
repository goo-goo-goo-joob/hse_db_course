import os

from PyQt5 import QtWidgets

from db_cinema_project.admin_cabinet import MainApp
from db_cinema_project.db import utils
from db_cinema_project.ui import auth_form


class AuthApp(QtWidgets.QMainWindow, auth_form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
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
            self.db = utils.DBCinema('localhost', os.getenv('DB_USER', login),
                                     os.getenv('DB_PASSWORD', password),
                                     'cinemadb')
            self.close()
            self.Open = MainApp(self.db)
            self.Open.show()
        # pylint: disable=W0703
        except Exception:  # runtime_error???
            self.msg.show()
