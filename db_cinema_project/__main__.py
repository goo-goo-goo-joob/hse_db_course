import sys
from PyQt5 import QtWidgets

from db_cinema_project.admin_auth import AuthApp
from db_cinema_project.ui import first_form
from db_cinema_project.user_auth import EnterApp
from db_cinema_project.user_registration import RegApp


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


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = FirstApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
