from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import Qt         

class MyComboBoxModel(QStringListModel):
    """Model for combo box items."""
    def __init__(self, items):
        super().__init__(items)
