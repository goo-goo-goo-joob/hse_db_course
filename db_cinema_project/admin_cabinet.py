from PyQt5 import QtWidgets

from db_cinema_project.ui import main, add_film
from db_cinema_project.utils.table import Table


class MainApp(QtWidgets.QMainWindow, main.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.print_db)
        self.add_film_btn.clicked.connect(self.fadd_film)
        self.db = db

    def fadd_film(self):
        self.Open = AddFilmApp(self.db)
        self.Open.show()

    def print_db(self):
        res = self.db.get_all_stuff()
        self.table = Table(res)
        self.table.show()


class AddFilmApp(QtWidgets.QMainWindow, add_film.Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        comunes = ['Ameglia', 'Arcola', 'Bagnone', 'Bolano', 'Carrara', 'Casola',
                   'Castelnuovo Magra',
                   'Comano, località Crespiano', 'Fivizzano',
                   'Fivizzano località Pieve S. Paolo',
                   'Fivizzano località Pieve di Viano', 'Fivizzano località Soliera',
                   'Fosdinovo', 'Genova',
                   'La Spezia', 'Levanto', 'Licciana Nardi', 'Lucca', 'Lusuolo',
                   'Massa',
                   'Minucciano',
                   'Montignoso', 'Ortonovo', 'Piazza al sercho', 'Pietrasanta',
                   'Pignine',
                   'Pisa',
                   'Podenzana', 'Pontremoli', 'Portovenere', 'Santo Stefano di Magra',
                   'Sarzana',
                   'Serravezza', 'Sesta Godano', 'Varese Ligure', 'Vezzano Ligure',
                   'Zignago']
        # self.comboBox = CheckableComboBox()
        self.comboBox.addItems(comunes)
        self.db = db
