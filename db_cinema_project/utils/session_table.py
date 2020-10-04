from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout

LastStateRole = QtCore.Qt.UserRole


class PlacesTable(QtWidgets.QMainWindow):
    def __init__(self, row, col, res, button_callback):
        super(PlacesTable, self).__init__()
        self.button_callback = button_callback
        self.title = 'Выбор мест'
        self.left = 0
        self.top = 0
        self.row = row
        self.col = col
        self.width = min(col * 75, 1900)
        self.height = min(row * 75, 900)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.tablewidget = QtWidgets.QTableWidget(row, col)
        self.submit_button = QtWidgets.QPushButton("Купить")
        self.submit_button.clicked.connect(self.get_places)

        self.widget = QWidget()
        layout = QGridLayout()
        self.widget.setLayout(layout)
        layout.addWidget(self.tablewidget)
        layout.addWidget(self.submit_button)
        self.setCentralWidget(self.widget)

        self.places = []

        header = self.tablewidget.horizontalHeader()
        for c in range(col):
            header.setSectionResizeMode(c, QtWidgets.QHeaderView.ResizeToContents)
        for row_data in res:
            item = QtWidgets.QTableWidgetItem()
            if row_data[2]:
                item.setBackground(QtGui.QColor(225, 26, 0))
            else:
                item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                item.setCheckState(QtCore.Qt.Unchecked)
                item.setBackground(QtGui.QColor(119, 221, 119))
            item.setData(LastStateRole, item.checkState())
            self.tablewidget.setItem(row_data[0] - 1, row_data[1] - 1, item)

    def get_places(self):
        self.places = []
        for r in range(self.row):
            for c in range(self.col):
                item = self.tablewidget.item(r, c)
                currentState = item.checkState()
                if currentState == QtCore.Qt.Checked:
                    self.places.append((r + 1, c + 1))
        self.button_callback(self.places)
