from PyQt5 import QtWidgets
from gui.generated.result_dialog import Ui_Dialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem


class ResultDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # Create a model with 3 rows, 2 columns
        columns = [
            "Series", "Size", "Ratio", "Limit for repeated peak torque [Nm]",
            "Limit for average torque [Nm]", "Rated torque at rated speed 2000 rpm [Nm]",
            "Limit for momentary peak torque [Nm]", "Max. input speed [rpm]",
            "Limit for average input speed [rpm]", "Moment of inertia [x10^-4]",
            "Weight"
        ]
        data_model = QStandardItemModel(5, 3)
        specs_model = QStandardItemModel(len(columns),1)

        # Set headers (optional)
        data_model.setHorizontalHeaderLabels(["Tourqe", "Angular Speed", "Timestamps"])
        data_model.setVerticalHeaderLabels(["1", "2", "3", "overload", "Dwell"])

        specs_model.setHorizontalHeaderLabels(["Specifications"])
        specs_model.setVerticalHeaderLabels(columns)
        # Attach model to your QTableView
        self.ui.viewTable.setModel(data_model)

        def fill_table(self, table, data):
            ''' Fill a QTableView with data 
            
            Parameters:
            table (QTableView): The table to fill
            data (list of list): 2D list containing the data to fill the table
            '''
            rows = table.rowCount()
            cols = table.columnCount()
            for row in range(rows):
                for col in range(cols):
                    data_model.setItem(row, col, QStandardItem(str(data[row][col])))

            self.ui.viewTable.setModel(data_model)

