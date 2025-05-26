from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QStringListModel
from main_window import Ui_MainWindow
from ComboBoxModel import ComboBoxModel




from PyQt5.QtWidgets import QMainWindow
from DataModel import DataModel
from PaymentStruct import PaymentStruct  # update as needed




class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Model-Based GUI Example")
        self.resize(800, 600)

        self.setup_models()

    def setup_models(self):
        # Set up Struct-based ComboBoxModel
        self.combo_model = ComboBoxModel(PaymentStruct, self.ui.comboBox)
        self.combo_model.fill_combo("all")  # or any SQL you want

        # Connect ComboBox selection to action (optional)
        self.ui.comboBox.currentIndexChanged.connect(self.on_combo_changed)

        # Set up Struct-based TableModel
        self.table_model = DataModel(PaymentStruct, self.ui.tableView)
        self.table_model.fill_table_with("all")  # or instance.get_all_query()

        # Optional table view tweaks
        self.ui.tableView.setAlternatingRowColors(True)
        self.ui.tableView.setSelectionBehavior(self.ui.tableView.SelectRows)
        self.ui.tableView.setEditTriggers(self.ui.tableView.NoEditTriggers)
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)

    def on_combo_changed(self, index):
        selected = self.combo_model.getSelectedItem()
        print("Selected item:", selected)
def main():
    import sys
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
