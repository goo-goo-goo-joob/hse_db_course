from PyQt5 import QtWidgets, QtGui

from db_cinema_project.db.utils import DBException
from db_cinema_project.ui import main, add_film, genre
from db_cinema_project.utils.table import Table


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_db)
        self.add_film_btn.clicked.connect(self.fadd_film)
        self.add_genre_btn.clicked.connect(self.fadd_genre)
        self.open_genre_btn.clicked.connect(self.fopen_genre)
        self.db = db

    def delete_genre(self, id_):
        try:
            self.db.delete_one_genre(id_)
            self.fopen_genre()
        except DBException as e:
            text, *_ = e.args
            self.msg.setText(text)
            self.msg.show()

    def change_genre(self, id_):
        data = self.db.get_one_genre(id_)
        self.Open = AddGenreApp(self.db, data, on_close=self.fopen_genre)
        self.Open.show()

    def fopen_genre(self):
        res, names = self.db.get_all_genre()
        self.table = Table(res, names, self.change_genre, "Обновить", self.delete_genre,
                           "Удалить")
        self.table.show()

    def fadd_genre(self):
        self.Open = AddGenreApp(self.db, on_close=self.fopen_genre)
        self.Open.show()

    def fadd_film(self):
        self.Open = AddFilmApp(self.db)
        self.Open.show()

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
        if data:
            self.lineEdit.setText(data[1])
            self.pushButton.setText("Изменить жанр")
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setWindowTitle("Ошибка добавления жанра")
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
                else:
                    self.db.add_genre(name)
                self.msg.setWindowTitle("Сообщение о добавлении")
                self.msg.setText("Жанр успешно добавлен.")
                self.msg.show()
            except DBException as e:
                text, *_ = e.args
                self.msg.setText(text)
                self.msg.show()


class AddFilmApp(QtWidgets.QMainWindow, add_film.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.db = db

        genres, _ = self.db.get_all_genre()
        genres_text = []
        genres_data = []
        for g in genres:
            genres_data.append(g[0])
            genres_text.append(g[1])
        self.comboBox.addItems(genres_text, genres_data)

        self.pushButton.clicked.connect(self.submit)

    def submit(self):
        print(self)
