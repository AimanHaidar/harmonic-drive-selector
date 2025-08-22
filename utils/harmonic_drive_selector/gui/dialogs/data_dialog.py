from PyQt5 import QtWidgets
from gui.generated.data_dialog import Ui_Dialog

class DataDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.dataTable.hide()
        self.ui.file_path.hide()
        self.ui.array_s.clicked.connect(self.show_table)
        self.ui.json_s.clicked.connect(self.show_file_path)
    
    def show_table(self):
        self.ui.dataTable.show()
        self.ui.file_path.hide()

    def show_file_path(self):
        self.ui.file_path.show()
        self.ui.dataTable.hide()