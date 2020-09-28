from PyQt5 import QtWidgets

from db_cinema_project.ui import lk_form
from db_cinema_project.utils.table import Table


class LKApp(QtWidgets.QMainWindow, lk_form.Ui_MainWindow):
    def __init__(self, db, uid):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.id = uid
        self.name = self.db.get_user_name_by_id(uid)
        self.label.setText(f'Приветствуем Вас, {self.name}')
        self.pushButton.clicked.connect(self.print_db)

    def print_db(self):
        res = self.db.get_all_user_numbers()
        self.table = Table(res)
        self.table.show()
