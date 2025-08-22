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
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.clicked.connect(self.insert_data)
    
    def show_table(self):
        self.ui.dataTable.show()
        self.ui.file_path.hide()

    def show_file_path(self):
        self.ui.file_path.show()
        self.ui.dataTable.hide()

    def insert_data(self):
        for row in range(self.ui.dataTable.rowCount()):
            for col in range(self.ui.dataTable.columnCount()):
                if row==self.ui.dataTable.rowCount()-1 and col == 0:
                    continue
                if row==self.ui.dataTable.rowCount()-1 and col == 1:
                    continue
                item = self.ui.dataTable.item(row, col)
                if item is None or item.text() == "":
                    print(f"Empty cell at ({row+1},{col+1})")
                    return
                try:
                    float(item.text())
                except ValueError:
                    print(f"Invalid float at ({row+1},{col+1}): {item.text()}")
                    return
        self.accept()