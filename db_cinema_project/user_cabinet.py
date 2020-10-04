from PyQt5 import QtWidgets

from db_cinema_project.db.utils import DBException
from db_cinema_project.ui import lk_form, buy_on_cinema, day_form
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
        self.film_btn.clicked.connect(self.buy_onfilm)
        self.tickets.clicked.connect(self.show_tickets)

        self.OpenBuyCinema = None
        self.OpenDate = None
        self.table_film = None
        self.table_tickets = None
        self.table_buy = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Не удалось выполнить операцию.")
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def show_tickets(self):
        res, names = self.db.get_user_tikets(self.uid)
        if res:
            self.table_buy = Table(res, names, table_title="Таблица покупок")
            self.table_buy.show()
        else:
            if self.table_buy:
                self.table_buy.close()
            self.msg.setText("У Вас еще нет покупок.")
            self.msg.show()

    def buy_onfilm(self):
        res, names = self.db.get_allsession_film()
        if res:
            self.table_film = Table(res, names, self.open_date, "Выбрать",
                                    table_title="Таблица фильмов")
            self.table_film.show()
        else:
            if self.table_film:
                self.table_film.close()
            self.msg.setText("Нет фильмов для просмотра.")
            self.msg.show()

    def open_date(self, idfilm):
        if not len(self.db.get_all_session()[0]):
            self.msg.setText("Нет сеансов для просмотра.")
            self.msg.show()
        else:
            self.OpenDate = OpenDateApp(self.db, self.uid, idfilm)
            self.OpenDate.show()

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
        self.table_session1 = None
        self.table_places = None

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
            res, names = self.db.get_all_session_bycinematime(cinema, date)
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
        self.idsess = idsess
        row, col = self.db.get_session_rowcol(idsess)
        res = self.db.get_sessionplaces(idsess)
        self.table_places = PlacesTable(row, col, res, self.message)
        self.table_places.show()

    def message(self, places):
        if not len(places):
            self.msg.setText('Выберите места.')
            self.msg.show()
        else:
            self.table_places.close()
            try:
                self.db.buy_places(self.idsess, places, self.uid)
                self.msg.setText(
                    "Билеты успешно забронированы. Счет на оплату поступит на Вашу почту.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class OpenDateApp(QtWidgets.QMainWindow, day_form.Ui_MainWindow):
    def __init__(self, db, uid, idfilm):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_cinema_session)
        self.db = db
        self.uid = uid
        self.idfilm = idfilm
        self.table_places = None
        self.table_session1 = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def open_cinema_session(self):
        date = self.date.selectedDate().toString('yyyy-MM-dd')
        if not date:
            self.msg.setText("Выберите дату.")
            self.msg.show()
        else:
            self.db.delete_old_session()
            res, names = self.db.get_all_session_byfilmtime(self.idfilm, date)
            if res:
                self.table_session1 = Table(res, names, button_edit=self.buy_form,
                                            button_edit_text="Выбрать места",
                                            table_title="Выбор сеансов")
                self.table_session1.show()
            else:
                if self.table_session1:
                    self.table_session1.close()
                self.msg.setText("На указанную дату нет просмотров выбранного фильма.")
                self.msg.show()

    def buy_form(self, idsess):
        self.idsess = idsess
        row, col = self.db.get_session_rowcol(idsess)
        res = self.db.get_sessionplaces(idsess)
        self.table_places = PlacesTable(row, col, res, self.message)
        self.table_places.show()

    def message(self, places):
        if not len(places):
            self.msg.setText('Выберите места.')
            self.msg.show()
        else:
            self.table_places.close()
            try:
                self.db.buy_places(self.idsess, places, self.uid)
                self.msg.setText(
                    "Билеты успешно забронированы. Счет на оплату поступит на Вашу почту.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()
