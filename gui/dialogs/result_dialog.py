from PyQt5 import QtWidgets
from gui.generated.result_dialog import Ui_Dialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTimer

class ResultDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        QTimer.singleShot(0, self.center_on_screen)
        # Create a model
        columns = [
            "Series", "Size", "Ratio", "Limit for repeated peak torque [Nm]",
            "Limit for average torque [Nm]", "Rated torque at rated speed 2000 rpm [Nm]",
            "Limit for momentary peak torque [Nm]", "Max. input speed [rpm]",
            "Limit for average input speed [rpm]", "Moment of inertia [x10^-4]",
            "Weight (standard version,light version) [kg]","Resonance frequency [Hz]",
        ]
        self.torque_data_model = QStandardItemModel(5, 3)
        self.tilting_force_data_model = QStandardItemModel(4, 6)
        self.specs_model = QStandardItemModel(len(columns),1)

        # Set headers for torque data
        self.torque_data_model.setHorizontalHeaderLabels(["torque (N.m)", "Angular Speed (rpm)", "Timestamps(sec)"])
        self.torque_data_model.setVerticalHeaderLabels(["1", "2", "3", "overload", "Dwell"])

        # Set headers for tilting force data
        self.tilting_force_data_model.setHorizontalHeaderLabels(["Fr (N)", "Lr (m)", "Fa (N)", "La (m)", "n (rpm)", "dt (s)"])
        self.tilting_force_data_model.setVerticalHeaderLabels(["1", "2", "3", "max"])

        self.specs_model.setHorizontalHeaderLabels(["Specifications"])
        self.specs_model.setVerticalHeaderLabels(columns)
        # Attach model to your QTableView
        self.ui.dataTableView.setModel(self.torque_data_model)
        self.ui.driveTableView.setModel(self.specs_model)

        #connect boxButton of continue dimensioning to accept
        self.ui.continue_box_button.accepted.connect(self.accept)
        self.ui.continue_box_button.rejected.connect(self.reject)

        self.ui.force_button.hide()
        self.ui.torque_button.hide()
        
        self.ui.result_2.hide()
        self.ui.result_3.hide()


    def fill_table(self, model, table, data):
        ''' Fill a QTableView with data 
        
        Parameters:
        table (QTableView): The table to fill
        data (list of list): 2D list containing the data to fill the table
        '''
        rows = model.rowCount()
        cols = model.columnCount()
        for row in range(rows):
            for col in range(cols):
                model.setItem(row, col, QStandardItem(str(data[row][col])))

        table.setModel(model)

    def center_on_screen(self):
            frame_geometry = self.frameGeometry()
            screen = QtWidgets.QApplication.primaryScreen()
            center_point = screen.availableGeometry().center()
            frame_geometry.moveCenter(center_point)
            self.move(frame_geometry.topLeft())
