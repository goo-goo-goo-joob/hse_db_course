from PyQt5 import QtWidgets
from PyQt5.uic.Compiler.qtproxies import QtGui

from db_cinema_project.db.utils import DBException
from db_cinema_project.ui import lk_form, buy_on_cinema
from db_cinema_project.utils.table import Table
from db_cinema_project.utils.session_table import PlacesTable


class LKApp(QtWidgets.QMainWindow, lk_form.Ui_MainWindow):
    def __init__(self, db, uid):
        super().__init__()
        self.setupUi(self)
        self.db = db
        self.uid = uid
        self.name = self.db.get_user_name_by_id(uid)
        self.label.setText(f'Приветствуем Вас, {self.name}')
        self.cinema_btn.clicked.connect(self.buy_bycinema)

        self.OpenBuyCinema = None
        self.table_session1 = None
        self.table_places = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Не удалось выполнить операцию.")
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def buy_bycinema(self):
        if not len(self.db.get_all_session()[0]):
            self.msg.setText("Нет сеансов для просмотра.")
            self.msg.show()
        else:
            self.OpenBuyCinema = OpenBuyCinemaApp(self.db, self.uid)
            self.OpenBuyCinema.show()


class OpenBuyCinemaApp(QtWidgets.QMainWindow, buy_on_cinema.Ui_MainWindow):
    def __init__(self, db, uid):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_cinema_session)
        self.db = db
        self.uid = uid

        allcinema, _ = self.db.get_all_cinema()
        cinema_text = []
        for c in allcinema:
            cinema_text.append(c[2])
        self.cinema.clear()
        self.cinema.addItems(cinema_text)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def open_cinema_session(self):
        cinema = self.cinema.currentText()
        cinema = cinema if cinema else None
        date = self.date.text()
        if not cinema:
            self.msg.setText("Выберите кинотеатр.")
            self.msg.show()
        elif not date:
            self.msg.setText("Выберите дату.")
            self.msg.show()
        else:
            self.db.delete_old_session()
            # todo : нормальную функцию для сеансов, передаем время и кинотеатр
            res, names = self.db.get_all_session()
            if res:
                self.table_session1 = Table(res, names, button_edit=self.buy_form,
                                            button_edit_text="Выбрать места",
                                            table_title="Выбор сеансов")
                self.table_session1.show()
            else:
                if self.table_session1:
                    self.table_session1.close()
                self.msg.setText("В указанном кинотеатре нет сеансов на выбранную дату.")
                self.msg.show()

    def buy_form(self, idsess):
        row, col = self.db.get_session_rowcol(idsess)
        res = self.db.get_sessionplaces(idsess)
        self.table_places = PlacesTable(row, col, res, self.message)
        self.table_places.show()

    def message(self, places):
        self.table_places.close()
        self.msg.setText("Билеты успешно куплены.")
        self.msg.show()