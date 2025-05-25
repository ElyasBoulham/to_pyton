from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QStringListModel
from main_window import Ui_MainWindow




class MyComboBoxModel(QStringListModel):
    """Model for combo box items, similar to DefaultComboBoxModel in Java."""
    def __init__(self, items):
        super().__init__(items)


class MyTableModel(QStandardItemModel):
    """Model for table, similar to AbstractTableModel."""
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


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Model-Based GUI Example")
        self.resize(800, 600)

        self.setup_models()

    def setup_models(self):
        # Combo box data
        combo_items = ["Option A", "Option B", "Option C"]
        combo_model = MyComboBoxModel(combo_items)
        self.ui.comboBox.setModel(combo_model)

        # Table data
        table_headers = ["Name", "Value"]
        table_data = [
            ["Item 1", 100],
            ["Item 2", 200],
            ["Item 3", 300],
        ]
        table_model = MyTableModel(table_data, table_headers)
        self.ui.tableView.setModel(table_model)
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setSelectionBehavior(self.ui.tableView.SelectRows)
        self.ui.tableView.setEditTriggers(self.ui.tableView.NoEditTriggers)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)


def main():
    import sys
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
