from PyQt5.QtWidgets import QTableView, QHeaderView
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class Struct:
    def __init__(self, id: int = -1):
        self.id = id
        self.DBTname = "`table`"
        self.column_names = []

    def get_id(self):
        return self.id

    def set_id(self, new_id):
        self.id = new_id

    def get_column_names(self):
        return self.column_names

    def set_column_names(self, names):
        self.column_names = names

    def get_DB_table_name(self):
        return self.DBTname

    def set_DB_table_name(self, name):
        self.DBTname = name

    def to_string(self):
        return "null"

    def to_search(self):
        return "null"

    def get_total_price(self):
        return 0

    def get_empty_instance(self):
        return Struct(-1)

    def set_prepared_statement(self, cursor):
        pass

    def get_delete_message(self):
        return "do you want to delete"

    def set_paint(self, obj, value, row, column):
        pass

    def set_to_paint(self, row, column):
        return None

    def get_all_query(self):
        return f"SELECT * FROM {self.DBTname} ORDER BY id"

    def get_delete_query(self, id_name):
        return f"DELETE FROM {self.DBTname} WHERE {id_name} = ?"

    def get_insert_query(self):
        return ""

    def get_update_query(self):
        return ""

    def get_upload_query(self, id_name):
        return f"SELECT * FROM {self.DBTname} WHERE {id_name} = ?"

    def get_filter_one_query(self, id_value, id_name):
        return f"SELECT * FROM {self.DBTname} WHERE {id_name} = '{id_value}' ORDER BY id"

    def get_filter_set_query(self, ids, id_name):
        return f"SELECT * FROM {self.DBTname} WHERE {id_name} IN ({ids}) ORDER BY id"

    def get_filter_from_query(self, subquery, id_value, id_name):
        return f"SELECT * FROM ({subquery}) AS sub WHERE {id_name} = {id_value} ORDER BY id"

    def get_group_by_year_query(self, date_column):
        return f"SELECT * FROM {self.DBTname} GROUP BY YEAR({date_column}) ORDER BY YEAR({date_column})"

    def set_column_widths(self, table: QTableView):
        """Set font and alignment for headers and cells."""
        header = table.horizontalHeader()
        font = QFont("Arial", 11, QFont.Bold)
        header.setFont(font)

        for col in range(table.model().columnCount()):
            header.setSectionResizeMode(col, QHeaderView.Stretch)
            table.setColumnWidth(col, 120)

        # Optional: set alignment via delegate or style sheets
        table.setStyleSheet("""
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                font-weight: bold;
                text-align: right;
            }
            QTableView::item {
                text-align: right;
            }
        """)
