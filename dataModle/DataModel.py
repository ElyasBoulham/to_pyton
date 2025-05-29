from PyQt5.QtCore import Qt, QAbstractTableModel
import pymysql
import configparser


class DataModel(QAbstractTableModel):
    def __init__(self, struct_cls, table_view=None):
        super().__init__()
        self.struct_cls = struct_cls
        self.instance = struct_cls()
        self.data = []
        self.table_view = table_view
        self.search_word = ""
        self.sqlquery = "none"

        if self.table_view:
            self.table_view.setModel(self)

    def rowCount(self, parent=None):
        return len(self.data)

    def columnCount(self, parent=None):
        return len(self.instance.getColumnNames())

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole:
            return str(self.data[row].set_to_paint(col))
        

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.instance.getColumnNames()[section]
        return None

    def getRow(self, row):
        return self.data[row]

    def getSelectedRow(self):
        if self.table_view:
            return self.table_view.currentIndex().row()
        return -1

    def setSelectByIndex(self, index):
        if self.table_view:
            self.table_view.selectRow(index)

    def setSelectById(self, id_):
        for i, item in enumerate(self.data):
            if item.getId() == id_:
                self.setSelectByIndex(i)
                return item
        return None

    def getInstance(self):
        return self.instance

    def update(self):
        self.layoutChanged.emit()
        if self.table_view and hasattr(self.instance, "setColumnWidths"):
            self.instance.setColumnWidths(self.table_view)

    def set_previous_state(self):
        self.reset_table(self.sqlquery, save=False)
        self.update()

    def reset_table(self, query, save=True):
        if query == "none":
            self.beginResetModel()
            self.data.clear()
            self.endResetModel()
            return

        config = configparser.ConfigParser()
        config.read("config.properties")

        connection = pymysql.connect(
            host=config["db"]["url"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            database=config["db"]["dbname"],
            charset="utf8mb4"
        )
              
        try:
            with connection.cursor() as cursor:
                sql = self.instance.get_all_query() if query == "all" else query
                cursor.execute(sql)
                rows = cursor.fetchall()

                self.beginResetModel()
                self.data.clear()



                
                for row in rows:
                    struct_obj = self.struct_cls().from_result_set(row)
                    self.data.append(struct_obj)
                self.endResetModel()

                if save:
                    self.sqlquery = query

                if self.table_view:
                    self.table_view.reset()

        finally:
            connection.close()

    def fill_table_with(self, query):
        self.reset_table(query, save=True)
        self.update()
