from PyQt5 import QtWidgets

from db_cinema_project.db.utils import DBException
from db_cinema_project.ui import lk_form, buy_on_cinema, day_form, film_genre, film_desc, \
    cheap_form
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
        self.cinema2_btn.clicked.connect(self.open_cinema)
        self.film_btn.clicked.connect(self.buy_onfilm)
        self.tickets.clicked.connect(self.show_tickets)
        self.filmgenre_btn.clicked.connect(self.open_filmgenre)
        self.filmdesc_btn.clicked.connect(self.open_descfilm)
        self.variety_btn.clicked.connect(self.open_variety)
        self.cheap_btn.clicked.connect(self.open_cheap)

        self.OpenBuyCinema = None
        self.OpenDate = None
        self.OpenFilmGenre = None
        self.OpenDescFilm = None
        self.OpenCheap = None
        self.table_film = None
        self.table_tickets = None
        self.table_buy = None
        self.table_genre = None
        self.table_variety = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Не удалось выполнить операцию.")
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def open_cinema(self):
        self.db.delete_old_session()
        res, names = self.db.get_all_cinema2()
        if res:
            self.table_cinema = Table(res, names, table_title="Таблица кинотеатров")
            self.table_cinema.show()
        else:
            if self.table_cinema:
                self.table_cinema.close()
            self.msg.setText("У нас пока нет кинотеатров.")
            self.msg.show()

    def open_variety(self):
        self.db.delete_old_session()
        res, names = self.db.get_variety()
        if res:
            self.table_variety = Table(res, names,
                                       table_title="Информация на ближайшую неделю")
            self.table_variety.show()
        else:
            if self.table_variety:
                self.table_variety.close()
            self.msg.setText("У нас пока нет сеансов.")
            self.msg.show()

    def show_tickets(self):
        self.db.delete_old_session()
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
        self.db.delete_old_session()
        res, names = self.db.get_allsession_film()
        if res:
            self.table_film = Table(res, names, self.open_genre, "Жанры",
                                    self.open_date, "Выбрать",
                                    table_title="Таблица фильмов")
            self.table_film.show()
        else:
            if self.table_film:
                self.table_film.close()
            self.msg.setText("Нет фильмов для просмотра.")
            self.msg.show()

    def open_genre(self, idfilm):
        res, names = self.db.get_genre_film(idfilm)
        if res:
            self.table_genre = Table(res, names, table_title="Жанры фильма")
            self.table_genre.show()
        else:
            if self.table_genre:
                self.table_genre.close()
            self.msg.setText("У фильма нет жанров.")
            self.msg.show()

    def open_date(self, idfilm):
        self.db.delete_old_session()
        if not len(self.db.get_all_session()[0]):
            self.msg.setText("Нет сеансов для просмотра.")
            self.msg.show()
        else:
            self.OpenDate = OpenDateApp(self.db, self.uid, idfilm)
            self.OpenDate.show()

    def open_cheap(self):
        self.db.delete_old_session()
        if not len(self.db.get_all_session()[0]):
            self.msg.setText("На этой неделе нет сеансов.")
            self.msg.show()
        else:
            self.OpenCheap = OpenCheapApp(self.db)
            self.OpenCheap.show()

    def buy_bycinema(self):
        self.db.delete_old_session()
        if not len(self.db.get_all_session()[0]):
            self.msg.setText("Нет сеансов для просмотра.")
            self.msg.show()
        else:
            self.OpenBuyCinema = OpenBuyCinemaApp(self.db, self.uid)
            self.OpenBuyCinema.show()

    def open_filmgenre(self):
        self.db.delete_old_session()
        if not len(self.db.get_all_film()[0]):
            self.msg.setText("Нет фильмов для подбора.")
            self.msg.show()
        else:
            self.OpenFilmGenre = OpenFilmGenreApp(self.db)
            self.OpenFilmGenre.show()

    def open_descfilm(self):
        self.db.delete_old_session()
        if not len(self.db.get_all_film()[0]):
            self.msg.setText("Нет фильмов для подбора.")
            self.msg.show()
        else:
            self.OpenDescFilm = OpenDescFilmApp(self.db)
            self.OpenDescFilm.show()


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
        self.open_cinema_session()

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
        self.open_cinema_session()

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
                self.msg.setText("На указанную дату нет сеансов выбранного фильма.")
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


class OpenFilmGenreApp(QtWidgets.QMainWindow, film_genre.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_table)
        self.db = db
        self.table_film = None

        allgenre, _ = self.db.get_all_genre1()
        genre_text = []
        for c in allgenre:
            genre_text.append(c[1])
        self.genre.clear()
        self.genre.addItems(genre_text)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def open_table(self):
        genre = self.genre.currentText()
        genre = genre if genre else None
        if not genre:
            self.msg.setText("Выберите жанр.")
            self.msg.show()
        else:
            res, names = self.db.get_genre_film2(genre)
            if res:
                self.table_film = Table(res, names, table_title="Таблица фильмов")
                self.table_film.show()
            else:
                if self.table_film:
                    self.table_film.close()
                self.msg.setText("Нет фильмов для выбранного жанра.")
                self.msg.show()


class OpenDescFilmApp(QtWidgets.QMainWindow, film_desc.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_table)
        self.db = db
        self.table_film = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def open_table(self):
        decsript = self.decsript.text()
        decsript = decsript if decsript else None
        if not decsript:
            self.msg.setText("Введите ключевую фразу.")
            self.msg.show()
        else:
            res, names = self.db.get_desc_film(decsript)
            if res:
                self.table_film = Table(res, names, table_title="Таблица фильмов")
                self.table_film.show()
            else:
                if self.table_film:
                    self.table_film.close()
                self.msg.setText("Нет фильмов для указанной ключевой фразы.")
                self.msg.show()


class OpenCheapApp(QtWidgets.QMainWindow, cheap_form.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_cheap)
        self.db = db
        self.table_cheap = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Информирование")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def open_cheap(self):
        spinBox = self.spinBox.text()
        money = spinBox if spinBox else None
        if not money:
            self.msg.setText("Введите максимульную цену.")
            self.msg.show()
        else:
            res, names = self.db.get_cheap_session(money)
            if res:
                self.table_cheap = Table(res, names,
                                         table_title="Самое дешевое на этой неделе")
                self.table_cheap.show()
            else:
                if self.table_cheap:
                    self.table_cheap.close()
                self.msg.setText("Нет подходящих кинотеатров.")
                self.msg.show()
