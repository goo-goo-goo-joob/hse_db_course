from PyQt5 import QtWidgets, QtGui, QtCore

from db_cinema_project.db.utils import DBException
from db_cinema_project.ui import main, add_film, genre, producer, restrict, typesess, \
    cinema, typehall, hall, session1, session2
from db_cinema_project.utils.table import Table


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)

        self.add_film_btn.clicked.connect(self.fadd_film)
        self.add_genre_btn.clicked.connect(self.fadd_genre)
        self.add_producer_btn.clicked.connect(self.fadd_producer)
        self.add_restrict_btn.clicked.connect(self.fadd_restrict)
        self.add_typesess_btn.clicked.connect(self.fadd_typesess)
        self.add_cinema_btn.clicked.connect(self.fadd_cinema)
        self.add_typehall_btn.clicked.connect(self.fadd_typehall)
        self.add_hall_btn.clicked.connect(self.fadd_hall)
        self.add_session_btn.clicked.connect(self.fadd_session)

        self.open_film_btn.clicked.connect(self.fopen_film)
        self.open_genre_btn.clicked.connect(self.fopen_genre)
        self.open_producer_btn.clicked.connect(self.fopen_producer)
        self.open_restrict_btn.clicked.connect(self.fopen_restrict)
        self.open_typesess_btn.clicked.connect(self.fopen_typesess)
        self.open_cinema_btn.clicked.connect(self.fopen_cinema)
        self.open_typehall_btn.clicked.connect(self.fopen_typehall)
        self.open_hall_btn.clicked.connect(self.fopen_hall)
        self.open_session_btn.clicked.connect(self.fopen_session)
        self.db = db
        self.table_film = None
        self.table_genre = None
        self.table_producer = None
        self.table_restrict = None
        self.table_typesess = None
        self.table_cinema = None
        self.table_typehall = None
        self.table_hall = None
        self.table_filmsess = None
        self.OpenGenre = None
        self.OpenProducer = None
        self.OpenRestrict = None
        self.OpenFilm = None
        self.OpenTypesess = None
        self.OpenCinema = None
        self.OpenTypehall = None
        self.OpenHall = None
        self.OpenSession = None

        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Не удалось выполнить операцию.")
        self.msg.setWindowTitle("Сообщение об ошибке")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def delete_film(self, id_):
        try:
            self.db.delete_one_film(id_)
            self.fopen_film()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_genre(self, id_):
        try:
            self.db.delete_one_genre(id_)
            self.fopen_genre()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_producer(self, id_):
        try:
            self.db.delete_one_producer(id_)
            self.fopen_producer()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_restrict(self, id_):
        try:
            self.db.delete_one_restrict(id_)
            self.fopen_restrict()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_typesess(self, id_):
        try:
            self.db.delete_one_typesess(id_)
            self.fopen_typesess()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_cinema(self, id_):
        try:
            self.db.delete_one_cinema(id_)
            self.fopen_cinema()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_typehall(self, id_):
        try:
            self.db.delete_one_typehall(id_)
            self.fopen_typehall()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_hall(self, id_):
        try:
            self.db.delete_one_hall(id_)
            self.fopen_hall()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def delete_session(self, id_):
        if self.db.number_bue_session(id_) > 0:
            self.msg.setText("Сеанс не может быть удален. На него уже куплены билеты.")
            self.msg.show()
        else:
            try:
                self.db.delete_one_session(id_)
                self.fopen_session()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()

    def change_film(self, id_):
        data = self.db.get_one_film(id_)
        self.OpenFilm = AddFilmApp(self.db, data, on_close=self.fopen_film)
        self.OpenFilm.show()

    def change_genre(self, id_):
        data = self.db.get_one_genre(id_)
        self.OpenGenre = AddGenreApp(self.db, data, on_close=self.fopen_genre)
        self.OpenGenre.show()

    def change_producer(self, id_):
        data = self.db.get_one_producer(id_)
        self.OpenProducer = AddProducerApp(self.db, data, on_close=self.fopen_producer)
        self.OpenProducer.show()

    def change_restrict(self, id_):
        data = self.db.get_one_restrict(id_)
        self.OpenRestrict = AddRestrictApp(self.db, data, on_close=self.fopen_restrict)
        self.OpenRestrict.show()

    def change_typesess(self, id_):
        data = self.db.get_one_typesess(id_)
        self.OpenTypesess = AddTypesessApp(self.db, data, on_close=self.fopen_typesess)
        self.OpenTypesess.show()

    def change_cinema(self, id_):
        data = self.db.get_one_cinema(id_)
        self.OpenCinema = AddCinemaApp(self.db, data, on_close=self.fopen_cinema)
        self.OpenCinema.show()

    def change_typehall(self, id_):
        data = self.db.get_one_typehall(id_)
        self.OpenTypehall = AddTypehallApp(self.db, data, on_close=self.fopen_typehall)
        self.OpenTypehall.show()

    def change_hall(self, id_):
        data = self.db.get_one_hall(id_)
        self.OpenHall = AddHallApp(self.db, data, on_close=self.fopen_hall)
        self.OpenHall.show()

    def change_session(self, id_):
        data = self.db.get_one_session(id_)
        self.OpenSession = AddSessionApp(self.db, data=data, film=data[-1], on_close=self.fopen_session)
        self.OpenSession.show()

    def fopen_film(self):
        res, names = self.db.get_all_film()
        if res:
            self.table_film = Table(res, names, self.change_film, "Обновить",
                                    self.delete_film,
                                    "Удалить", "Таблица фильмов")
            self.table_film.show()
        else:
            if self.table_film:
                self.table_film.close()
            self.msg.setText("Нет фильмов для просмотра.")
            self.msg.show()

    def fopen_genre(self):
        res, names = self.db.get_all_genre()
        if res:
            self.table_genre = Table(res, names, self.change_genre, "Обновить",
                                     self.delete_genre,
                                     "Удалить", "Таблица жанров")
            self.table_genre.show()
        else:
            if self.table_genre:
                self.table_genre.close()
            self.msg.setText("Нет жанров для просмотра.")
            self.msg.show()

    def fopen_producer(self):
        res, names = self.db.get_all_producer()
        if res:
            self.table_producer = Table(res, names, self.change_producer, "Обновить",
                                        self.delete_producer, "Удалить",
                                        "Таблица режиссеров")
            self.table_producer.show()
        else:
            if self.table_producer:
                self.table_producer.close()
            self.msg.setText("Нет режиссеров для просмотра.")
            self.msg.show()

    def fopen_restrict(self):
        res, names = self.db.get_all_restrict()
        if res:
            self.table_restrict = Table(res, names, self.change_restrict, "Обновить",
                                        self.delete_restrict, "Удалить",
                                        "Таблица ограничений")
            self.table_restrict.show()
        else:
            if self.table_restrict:
                self.table_restrict.close()
            self.msg.setText("Нет ограничений для просмотра.")
            self.msg.show()

    def fopen_typesess(self):
        res, names = self.db.get_all_typesess()
        if res:
            self.table_typesess = Table(res, names, self.change_typesess, "Обновить",
                                        self.delete_typesess, "Удалить",
                                        "Таблица типов сеансов")
            self.table_typesess.show()
        else:
            if self.table_typesess:
                self.table_typesess.close()
            self.msg.setText("Нет типов сеансов для просмотра.")
            self.msg.show()

    def fopen_cinema(self):
        res, names = self.db.get_all_cinema()
        if res:
            self.table_cinema = Table(res, names, self.change_cinema, "Обновить",
                                      self.delete_cinema, "Удалить",
                                      "Таблица кинотеатров")
            self.table_cinema.show()
        else:
            if self.table_cinema:
                self.table_cinema.close()
            self.msg.setText("Нет кинотеатров для просмотра.")
            self.msg.show()

    def fopen_typehall(self):
        res, names = self.db.get_all_typehall()
        if res:
            self.table_typehall = Table(res, names, self.change_typehall, "Обновить",
                                        self.delete_typehall, "Удалить",
                                        "Таблица типов залов")
            self.table_typehall.show()
        else:
            if self.table_typehall:
                self.table_typehall.close()
            self.msg.setText("Нет типов залов для просмотра.")
            self.msg.show()

    def fopen_hall(self):
        res, names = self.db.get_all_hall()
        if res:
            self.table_hall = Table(res, names, self.change_hall, "Обновить",
                                    self.delete_hall, "Удалить",
                                    "Таблица залов")
            self.table_hall.show()
        else:
            if self.table_hall:
                self.table_hall.close()
            self.msg.setText("Нет залов для просмотра.")
            self.msg.show()

    def fopen_session(self):
        res, names = self.db.get_all_session()
        if res:
            self.table_session = Table(res, names, self.change_session, "Обновить",
                                    self.delete_session, "Удалить",
                                    "Таблица сеансов")
            self.table_session.show()
        else:
            if self.table_session:
                self.table_session.close()
            self.msg.setText("Нет сеансов для просмотра.")
            self.msg.show()

    def fadd_film(self):
        self.OpenFilm = AddFilmApp(self.db, on_close=self.fopen_film)
        self.OpenFilm.show()

    def fadd_genre(self):
        self.OpenGenre = AddGenreApp(self.db, on_close=self.fopen_genre)
        self.OpenGenre.show()

    def fadd_producer(self):
        self.OpenProducer = AddProducerApp(self.db, on_close=self.fopen_producer)
        self.OpenProducer.show()

    def fadd_restrict(self):
        self.OpenRestrict = AddRestrictApp(self.db, on_close=self.fopen_restrict)
        self.OpenRestrict.show()

    def fadd_typesess(self):
        self.OpenTypesess = AddTypesessApp(self.db, on_close=self.fopen_typesess)
        self.OpenTypesess.show()

    def fadd_cinema(self):
        self.OpenCinema = AddCinemaApp(self.db, on_close=self.fopen_cinema)
        self.OpenCinema.show()

    def fadd_typehall(self):
        self.OpenTypehall = AddTypehallApp(self.db, on_close=self.fopen_typehall)
        self.OpenTypehall.show()

    def fadd_hall(self):
        self.OpenHall = AddHallApp(self.db, on_close=self.fopen_hall)
        self.OpenHall.show()

    def fadd_session(self):
        res, names = self.db.get_all_film()
        if res:
            self.table_filmsess = Table(res, names, self.add_session_form, "Задать сеанс",
                                        table_title="Таблица фильмов")
            self.table_filmsess.show()
        else:
            if self.table_filmsess:
                self.table_filmsess.close()
            self.msg.setText("Нет фильмов для назначения сеанса.")
            self.msg.show()

    def add_session_form(self, film):
        self.OpenSession = AddSessionApp(db=self.db,
                                         film=film, on_close=self.fopen_session)
        self.OpenSession.show()
        self.table_filmsess.close()

    def print_db(self):
        res = self.db.get_all_stuff()
        self.table = Table(res)
        self.table.show()


class AddGenreApp(QtWidgets.QMainWindow, genre.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_genre_db)
        self.db = db
        self.data = data
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления жанра")
        if data:
            self.lineEdit.setText(data[1])
            self.pushButton.setText("Изменить жанр")
            self.msg.setWindowTitle("Ошибка изменения жанра")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def ok(self):
        self.msg.close()

    def add_genre_db(self):
        name = self.lineEdit.text()
        name = name.lower() if name else None
        if not name:
            self.msg.setText("Введите название жанра.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_genre(self.data[0], name)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Жанр успешно изменен.")
                else:
                    self.db.add_genre(name)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Жанр успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddProducerApp(QtWidgets.QMainWindow, producer.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_producer_db)
        self.db = db
        self.data = data
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления режиссера")
        if data:
            self.lineEdit.setText(data[1])
            self.pushButton.setText("Изменить ФИО режиссера")
            self.msg.setWindowTitle("Ошибка изменения ФИО режиссера")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_producer_db(self):
        name = self.lineEdit.text()
        name = name.lower() if name else None
        if not name:
            self.msg.setText("Введите ФИО режиссера.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_producer(self.data[0], name)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Режиссер успешно изменен.")
                else:
                    self.db.add_producer(name)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Режиссер успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddRestrictApp(QtWidgets.QMainWindow, restrict.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_restrict_db)
        self.db = db
        self.data = data
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления ограничения")
        if data:
            self.lineEdit.setText(data[1])
            self.pushButton.setText("Изменить ограничение")
            self.msg.setWindowTitle("Ошибка изменения ограничения")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_restrict_db(self):
        name = self.lineEdit.text()
        name = name.lower() if name else None
        if not name:
            self.msg.setText("Введите ограничение.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_restrict(self.data[0], name)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Ограничение успешно изменено.")
                else:
                    self.db.add_restrict(name)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Ограничение успешно добавлено.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddTypesessApp(QtWidgets.QMainWindow, typesess.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_typesess_db)
        self.db = db
        self.data = data
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления типа сеанса")
        if data:
            self.name.setText(data[1])
            self.beginTime.setTime(
                QtCore.QTime(data[2].seconds // 3600, data[2].seconds % 3600 // 60, 0))
            self.endTime.setTime(
                QtCore.QTime(data[3].seconds // 3600, data[3].seconds % 3600 // 60, 0))
            self.additon.setValue(data[4])
            self.pushButton.setText("Изменить тип сеанса")
            self.msg.setWindowTitle("Ошибка изменения типа сеанса")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_typesess_db(self):
        name = self.name.text()
        start = self.beginTime.text()
        end = self.endTime.text()
        additon = self.additon.text()
        name = name.lower() if name else None
        start = start if start else None
        end = end if end else None
        additon = additon if additon else None
        if not name:
            self.msg.setText("Введите название типа сеанса.")
            self.msg.show()
        elif not start:
            self.msg.setText("Введите начало типа сеанса.")
            self.msg.show()
        elif not end:
            self.msg.setText("Введите конец типа сеанса.")
            self.msg.show()
        elif not additon:
            self.msg.setText("Введите надбавку типа сеанса.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_typesess(self.data[0], name, start, end, additon)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Тип сеанса успешно изменен.")
                else:
                    self.db.add_typesess(name, start, end, additon)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Тип сеанса успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddCinemaApp(QtWidgets.QMainWindow, cinema.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_cinema_db)
        self.db = db
        self.data = data
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления кинотеатра")
        if data:
            self.name.setText(data[1])
            self.address.setText(data[2])
            self.price.setValue(data[3])
            self.pushButton.setText("Изменить кинотеатр")
            self.msg.setWindowTitle("Ошибка изменения кинотеатра")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_cinema_db(self):
        name = self.name.text()
        address = self.address.text()
        price = self.price.text()
        name = name.lower() if name else None
        address = address.lower() if address else None
        price = price if price else None
        if not name:
            self.msg.setText("Введите название кинотеатра.")
            self.msg.show()
        elif not address:
            self.msg.setText("Введите адрес кинотеатра.")
            self.msg.show()
        elif not price:
            self.msg.setText("Введите базовую цену кинотеатра.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_cinema(self.data[0], name, address, price)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Кинотеатр успешно изменен.")
                else:
                    self.db.add_cinema(name, address, price)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Кинотеатр успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddTypehallApp(QtWidgets.QMainWindow, typehall.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_typehall_db)
        self.db = db
        self.data = data
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления типа зала")
        if data:
            self.name.setText(data[1])
            self.price.setValue(data[2])
            self.pushButton.setText("Изменить тип зала")
            self.msg.setWindowTitle("Ошибка изменения типа зала")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_typehall_db(self):
        name = self.name.text()
        price = self.price.text()
        name = name.lower() if name else None
        price = price if price else None
        if not name:
            self.msg.setText("Введите название типа зала.")
            self.msg.show()
        elif not price:
            self.msg.setText("Введите надбавку типа зала.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_typehall(self.data[0], name, price)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Тип зала успешно изменен.")
                else:
                    self.db.add_typehall(name, price)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Тип зала успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddHallApp(QtWidgets.QMainWindow, hall.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_hall_db)
        self.db = db
        self.data = data
        self.on_close = on_close

        alltypehall, _ = self.db.get_all_typehall()
        allcinema, _ = self.db.get_all_cinema()
        typehall_text = []
        cinema_text = []
        for t in alltypehall:
            typehall_text.append(t[1])
        for c in allcinema:
            cinema_text.append(c[2])
        self.typehall.clear()
        self.typehall.addItems(typehall_text)
        self.cinema.clear()
        self.cinema.addItems(cinema_text)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления зала")
        if data:
            self.name.setText(data[1])
            self.length.setValue(data[2])
            self.number.setValue(data[3])
            self.typehall.setCurrentText(self.db.get_one_typehall(data[4])[1])
            self.cinema.setCurrentText(self.db.get_one_cinema(data[5])[2])
            self.pushButton.setText("Изменить зал")
            self.msg.setWindowTitle("Ошибка изменения зала")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_hall_db(self):
        name = self.name.text()
        length = self.length.text()
        number = self.number.text()
        typehall = self.typehall.currentText()
        cinema = self.cinema.currentText()
        name = name.lower() if name else None
        length = length if length else None
        number = number if number else None
        typehall = typehall if typehall else None
        cinema = cinema if cinema else None
        if not name:
            self.msg.setText("Введите название зала.")
            self.msg.show()
        elif not length:
            self.msg.setText("Введите длину ряда зала.")
            self.msg.show()
        elif not number:
            self.msg.setText("Введите число рядов зала.")
            self.msg.show()
        elif not typehall:
            self.msg.setText("Выберите типа зала.")
            self.msg.show()
        elif not cinema:
            self.msg.setText("Выберите кинотеатр.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_hall(self.data[0], name, length, number,
                                        self.db.get_id_typehall(typehall),
                                        self.db.get_id_cinema(cinema))
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Зал успешно изменен.")
                else:
                    self.db.add_hall(name, length, number,
                                     self.db.get_id_typehall(typehall),
                                     self.db.get_id_cinema(cinema))
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Зал успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddFilmApp(QtWidgets.QMainWindow, add_film.Ui_MainWindow):
    def __init__(self, db, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.add_film_db)
        self.db = db
        self.data = data
        self.on_close = on_close

        allgenre = self.db.get_all_genre()[0]
        allproducer = self.db.get_all_producer()[0]
        allrestrict = self.db.get_all_restrict()[0]
        alltypehall = self.db.get_all_typehall()[0]
        genre_text = []
        genre_data = []
        producer_text = []
        restrict_text = []
        typehall_text = []
        typehall_data = []
        for t in allgenre:
            genre_text.append(t[1])
            genre_data.append(t[0])
        for t in allproducer:
            producer_text.append(t[1])
        for t in allrestrict:
            restrict_text.append(t[1])
        for t in alltypehall:
            typehall_text.append(t[1])
            typehall_data.append(t[0])
        self.genre.clear()
        self.genre.addItems(genre_text, genre_data)
        self.producer.clear()
        self.producer.addItems(producer_text)
        self.restrict.clear()
        self.restrict.addItems(restrict_text)
        self.typehall.clear()
        self.typehall.addItems(typehall_text, typehall_data)
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления фильма")
        if data:
            self.name.setText(data[1])
            self.descript.setPlainText(data[2])
            self.year.setValue(data[3])
            self.duration.setTime(
                QtCore.QTime(data[4].seconds // 3600, data[4].seconds % 3600 // 60, 0))
            self.producer.setCurrentText(self.db.get_one_producer(data[5])[1])
            self.restrict.setCurrentText(self.db.get_one_restrict(data[6])[1])
            self.genre.setTexts(self.db.get_film_genre(data[0]))
            self.typehall.setTexts(self.db.get_film_typehall(data[0]))
            self.pushButton.setText("Изменить фильм")
            self.msg.setWindowTitle("Ошибка изменения фильма")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def add_film_db(self):
        name = self.name.text()
        descript = self.descript.toPlainText()
        year = self.year.text()
        duration = self.duration.text()
        genre = self.genre.currentData()
        producer = self.producer.currentText()
        restrict = self.restrict.currentText()
        typehall = self.typehall.currentData()
        name = name.lower() if name else None
        descript = descript.lower() if descript else None
        year = year if year else None
        duration = duration if duration != '0:00' else None
        genre = genre if genre else None
        producer = producer if producer else None
        restrict = restrict if restrict else None
        typehall = typehall if typehall else None
        if not name:
            self.msg.setText("Введите название фильма.")
            self.msg.show()
        elif not descript:
            self.msg.setText("Введите описание фильма.")
            self.msg.show()
        elif not year:
            self.msg.setText("Введите год фильма.")
            self.msg.show()
        elif not duration:
            self.msg.setText("Введите продолжительность фильма.")
            self.msg.show()
        elif not genre:
            self.msg.setText("Выберите жанры.")
            self.msg.show()
        elif not producer:
            self.msg.setText("Выберите режиссера.")
            self.msg.show()
        elif not restrict:
            self.msg.setText("Выберите ограничение.")
            self.msg.show()
        elif not typehall:
            self.msg.setText("Выберите типы залов.")
            self.msg.show()
        else:
            try:
                if self.data:
                    self.db.update_film(self.data[0], name, descript, year, duration,
                                        genre, self.db.get_id_producer(producer),
                                        self.db.get_id_restrict(restrict), typehall)
                    self.msg.setWindowTitle("Сообщение об изменении")
                    self.msg.setText("Фильм успешно изменен.")
                else:
                    self.db.add_film(name, descript, year, duration,
                                     genre, self.db.get_id_producer(producer),
                                     self.db.get_id_restrict(restrict), typehall)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Фильм успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddSessionApp(QtWidgets.QMainWindow, session1.Ui_MainWindow):
    def __init__(self, db, film, data=None, *, on_close=None):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.load_halls)
        self.pushButton_2.clicked.connect(self.next_form)
        self.db = db
        self.data = data
        self.film = film
        self.on_close = on_close
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления сеанса")
        allcinema = self.db.get_all_cinema1(film)[0]
        cinema_text = []
        for t in allcinema:
            cinema_text.append(t[0])
        self.cinema.clear()
        self.cinema.addItems(cinema_text)
        self.hall.clear()
        if data:
            self.dateTime.setDateTime(data[1])
            self.cinema.setCurrentText(self.db.get_one_cinema1(data[2])[2])
            self.load_halls()
            self.hall.setCurrentText(self.db.get_one_hall(data[2])[1])
            self.pushButton_2.setText("Изменить сеанс")
            self.msg.setWindowTitle("Ошибка изменения сеанса")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.ok)

    def ok(self):
        self.msg.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.on_close:
            self.on_close()

    def load_halls(self):
        cinemahalls = self.db.get_allcinema_hall1(self.cinema.currentText(), self.film)
        self.hall.clear()
        self.hall.addItems(
            cinemahalls if isinstance(cinemahalls, str) else [c[0] for c in cinemahalls])

    def next_form(self):
        cinema = self.cinema.currentText()
        hall = self.hall.currentText()
        dateTime = self.dateTime.text()
        cinema = cinema if cinema else None
        hall = hall if hall else None
        if not cinema:
            self.msg.setText("Выберите кинотеатр.")
            self.msg.show()
        elif not hall:
            self.msg.setText("Выберите зал.")
            self.msg.show()
        elif not dateTime:
            self.msg.setText("Выберите время.")
            self.msg.show()
        elif not self.db.check_hallincinema(hall, cinema):
            self.msg.setText(
                "Нажмите на конопку \"Показать возможные залы\" и выберите зал.")
            self.msg.show()
        else:
            try:
                if self.data:
                    if not self.db.number_bue_session(self.data[0]):
                        self.db.update_session(self.data[0], self.db.get_id_hall(hall, cinema),
                                               dateTime, self.film)
                        self.msg.setWindowTitle("Сообщение об изменении")
                        self.msg.setText("Сеанс успешно изменен.")
                    else:
                        self.msg.setText("Сеанс не будет изменен, на него уже куплены билеты.")
                else:
                    self.db.add_session(self.db.get_id_hall(hall, cinema), dateTime, self.film)
                    self.msg.setWindowTitle("Сообщение о добавлении")
                    self.msg.setText("Сеанс успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()
