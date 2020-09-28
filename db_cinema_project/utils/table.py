from functools import partial

from PyQt5 import QtWidgets


class Table(QtWidgets.QWidget):
    def __init__(self, res, names=None, button_edit=None, button_edit_text=None,
                 button_delete=None, button_delete_text=None):
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
        self.tableWidget.setColumnCount(
            len(res[0]) - 1 + (button_edit is not None) + (button_delete is not None))

        if names is not None:
            horizontal_header = [x[0] for x in names[1:]]
            if button_edit_text:
                horizontal_header.append(button_edit_text)
            if button_delete_text:
                horizontal_header.append(button_delete_text)
            self.tableWidget.setHorizontalHeaderLabels(horizontal_header)

        for row_number, row_data in enumerate(res):
            for column_number, data in enumerate(row_data[1:]):
                self.tableWidget.setItem(row_number, column_number,
                                         QtWidgets.QTableWidgetItem(str(data)))
            if button_edit is not None:
                btn_edit = QtWidgets.QPushButton(button_edit_text)
                arg = row_data[0]
                btn_edit.clicked.connect(partial(button_edit, arg))
                self.tableWidget.setCellWidget(row_number, len(row_data[1:]), btn_edit)

            if button_delete is not None:
                btn_delete = QtWidgets.QPushButton(button_delete_text)
                arg = row_data[0]
                btn_delete.clicked.connect(partial(button_delete, arg))
                self.tableWidget.setCellWidget(row_number, len(row_data[1:]) + 1,
                                               btn_delete)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
