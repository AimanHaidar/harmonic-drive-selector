from PyQt5 import QtWidgets
from gui.generated.data_dialog import Ui_Dialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog
from PyQt5.QtWidgets import QTableWidgetItem

class DataDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.dataTable.hide()
        self.ui.file_path.hide()
        self.ui.label_2.hide()
        self.ui.array_s.clicked.connect(self.show_table)
        self.ui.json_s.clicked.connect(self.show_file_path)
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.insert_data)
        self.float_data = [[0 for _ in range(self.ui.dataTable.columnCount())] for _ in range(self.ui.dataTable.rowCount())]

        self.ui.dataTable.setItem(0, 0, QTableWidgetItem("400"))
        self.ui.dataTable.setItem(1, 0, QTableWidgetItem("320"))
        self.ui.dataTable.setItem(2, 0, QTableWidgetItem("200"))
        self.ui.dataTable.setItem(3, 0, QTableWidgetItem("1000"))

        # Second column
        self.ui.dataTable.setItem(0, 2, QTableWidgetItem("0.3"))
        self.ui.dataTable.setItem(1, 2, QTableWidgetItem("3.0"))
        self.ui.dataTable.setItem(2, 2, QTableWidgetItem("0.4"))
        self.ui.dataTable.setItem(3, 2, QTableWidgetItem("0.15"))
        self.ui.dataTable.setItem(4, 2, QTableWidgetItem("0.2"))

        # Third column
        self.ui.dataTable.setItem(0, 1, QTableWidgetItem("7"))
        self.ui.dataTable.setItem(1, 1, QTableWidgetItem("14"))
        self.ui.dataTable.setItem(2, 1, QTableWidgetItem("7"))
        self.ui.dataTable.setItem(3, 1, QTableWidgetItem("14"))

    def show_table(self):
        self.ui.dataTable.show()
        self.ui.file_path.hide()
        self.ui.label_2.hide()

    def show_file_path(self):
        self.ui.file_path.show()
        self.ui.dataTable.hide()
        self.ui.label_2.show()

    def insert_data(self):
        for col in range(self.ui.dataTable.columnCount()):
            for row in range(self.ui.dataTable.rowCount()):
                #skip last row first two columns for lifetime and pause time
                if row==self.ui.dataTable.rowCount()-1 and col == 0:
                    continue
                if row==self.ui.dataTable.rowCount()-1 and col == 1:
                    continue

                item = self.ui.dataTable.item(row, col)
                if item is None or item.text() == "":
                    print(f"Empty cell at ({row+1},{col+1})")
                    non_numbers_dialog = NonNumbersDialog()
                    non_numbers_dialog.exec_()
                    return
                
                try:
                    print(item.text())
                    self.float_data[row][col] = float(item.text())
                except ValueError:
                    print(f"Invalid float at ({row+1},{col+1}): {item.text()}")
                    non_numbers_dialog = NonNumbersDialog()
                    non_numbers_dialog.exec_()
                    return
        print(self.float_data)
        self.accept()