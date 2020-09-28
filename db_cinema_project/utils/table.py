from PyQt5 import QtWidgets


class Table(QtWidgets.QWidget):
    def __init__(self, res):
        super().__init__()
        self.title = 'Таблица'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 700

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(len(res))
        self.tableWidget.setColumnCount(len(res[0]))

        for row_number, row_data in enumerate(res):
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,
                                         QtWidgets.QTableWidgetItem(str(data)))

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
