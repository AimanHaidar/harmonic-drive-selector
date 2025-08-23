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
            "Weight (standard version,light version) [kg]",
        ]
        self.data_model = QStandardItemModel(5, 3)
        self.specs_model = QStandardItemModel(len(columns),1)

        # Set headers (optional)
        self.data_model.setHorizontalHeaderLabels(["torque (N.m)", "Angular Speed (rpm)", "Timestamps(sec)"])
        self.data_model.setVerticalHeaderLabels(["1", "2", "3", "overload", "Dwell"])

        self.specs_model.setHorizontalHeaderLabels(["Specifications"])
        self.specs_model.setVerticalHeaderLabels(columns)
        # Attach model to your QTableView
        self.ui.dataTableView.setModel(self.data_model)
        self.ui.driveTableView.setModel(self.specs_model)

    def fill_table(self, model, table, data):
        ''' Fill a QTableView with data 
        
        Parameters:
        table (QTableView): The table to fill
        data (list of list): 2D list containing the data to fill the table
        '''
        rows = model.rowCount()
        cols = model.columnCount()
        print("hell:",rows,cols)
        print(data)
        for row in range(rows):
            for col in range(cols):
                model.setItem(row, col, QStandardItem(str(data[row][col])))

        table.setModel(model)

