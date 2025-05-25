

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel       
from PyQt5.QtWidgets import QStandardItemModel
            


class MyTableModel(QStandardItemModel):
    """Model for table view."""
    def __init__(self, data, headers):
        super().__init__()
        self.setColumnCount(len(headers))
        self.setRowCount(len(data))
        self.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, value in enumerate(row_data):
                item = QStandardItem(str(value))
                item.setEditable(False)
                self.setItem(row_index, col_index, item)

