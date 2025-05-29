from PyQt5.QtCore import Qt, QAbstractListModel, QModelIndex
import pymysql
import configparser


class ComboBoxModel(QAbstractListModel):
    def __init__(self, struct_cls, combobox=None):
        super().__init__()
        self.struct_cls = struct_cls
        self.instance = self.struct_cls()
        self.items = [self.instance.getEmptyOne()]

        self.selectedItem = self.instance.getEmptyOne()
        self.sqlquery = ""
        self.searchWord = ""
        self.combobox = combobox


        if self.combobox != None:
            self.combobox.setModel(self)
            self.combobox.repaint()

    def rowCount(self, parent=QModelIndex()):
        return len(self.items)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and index.isValid():
            item = self.items[index.row()]
            return str(item)  # Ensure the string representation of the item is returned
        return None

    def clear(self):
        self.beginResetModel()
        self.items.clear()
        self.items.append(self.instance.getEmptyOne())
        self.endResetModel()

    def update(self):
        self.beginResetModel()
        self.endResetModel()
        if self.combobox:
            self.combobox.setCurrentIndex(0)

    def fill_combo(self, query):
        self.clear()
        self.reset_list(query, save=True)
        self.update()

    def reset_list(self, query, save=True):
        if query == "none":
            self.clear()
            return

        config = configparser.ConfigParser()
        config.read("config.properties")

        connection = pymysql.connect(
            host=config["db"]["url"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            database=config["db"]["dbname"]
        )

        try:
            with connection.cursor() as cursor:
                sql = self.instance.get_all_query() if query == "all" else query
                
                cursor.execute(sql)
                rows = cursor.fetchall()
             
                self.beginResetModel()
                self.items.clear()
                self.items.append(self.instance.getEmptyOne())
                for row in rows:
                    struct_obj=self.struct_cls().from_result_set(row)
                    self.items.append(struct_obj)
                if save:
                    self.sqlquery = query

                self.endResetModel()

                # Ensure the ComboBox is updated after filling
                if self.combobox:
                    self.combobox.setModel(self)
                    self.combobox.repaint()

        finally:
            connection.close()

    def filter(self, search):
        if self.searchWord not in search:
            self.reset_list(self.sqlquery, save=True)
        self.searchWord = search

        self.beginResetModel()
        self.items = [item for item in self.items if search.lower() in str(item.to_search()).lower()]
        self.endResetModel()
        self.update()

    def supprimer(self, id_):
        config = configparser.ConfigParser()
        config.read("config.properties")

        connection = pymysql.connect(
            host=config["db"]["url"],
            user=config["db"]["username"],
            password=config["db"]["password"],
            database=config["db"]["dbname"]
        )

        try:
            with connection.cursor() as cursor:
                sql = self.instance.get_delet_query("id")
                cursor.execute(sql, (id_,))
                if cursor.rowcount == 1:
                    self.reset_list(self.sqlquery, save=True)
                    self.update()
        finally:
            connection.close()

    def get_ids(self):
        return {str(item.getId()) for item in self.items}

    def filter_from_one(self, id_, nameid):
        self.reset_from_one(id_, nameid)
        self.update()

    def reset_from_one(self, id_, nameid):
        query = self.instance.get_filter_one_query(id_, nameid)
        self.reset_list(query, save=True)

    def filter_from_set(self, ids, nameid):
        self.reset_from_set(ids, nameid)
        self.update()

    def reset_from_set(self, ids, nameid):
        if not ids:
            self.reset_list("none", save=True)
            return

        s_ids = ",".join(ids)
        query = self.instance.get_filter_set_query(s_ids, nameid)
        self.reset_list(query, save=True)

    def filter_FROM_myqery(self, id_, nameid):
        if self.sqlquery != "none":
            query = self.instance.get_filter_FROM_myqery_query(self.sqlquery, id_, nameid)
            self.reset_list(query, save=False)
        self.update()

    def grouping_by(self, idname):
        query = self.instance.get_grouping_by(idname)
        self.reset_list(query, save=True)
        self.update()

    def selectById(self, id_):
        for i, item in enumerate(self.items):
            if item.getId() == id_:
                self.selectedItem = item
                if self.combobox:
                    self.combobox.setCurrentIndex(i)
                return item
        return None

    def getSelectedItem(self):
        return self.selectedItem
