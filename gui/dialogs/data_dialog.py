from PyQt5 import QtWidgets
from gui.generated.data_dialog import Ui_Dialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog
from gui.dialogs.force_info_dialog import ForceInfoDialog
from gui.dialogs.torque_info_dialog import TorqueInfoDialog
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QTimer, Qt

class DataDialog(QtWidgets.QDialog):
    def __init__(self,data_type, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        QTimer.singleShot(0, self.center_on_screen)
        self.ui.dataTable.hide()
        self.ui.file_path.hide()
        self.ui.label_2.hide()
        self.ui.array_s.clicked.connect(self.show_table)
        self.ui.json_s.clicked.connect(self.show_file_path)
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.insert_data)
        self.data_type = data_type
        self.ui.info_button.clicked.connect(self.show_info)
        # Fill table with example data
        if data_type == "torque":
            # First column T
            self.ui.dataTable.setItem(0, 0, QTableWidgetItem("400"))
            self.ui.dataTable.setItem(1, 0, QTableWidgetItem("320"))
            self.ui.dataTable.setItem(2, 0, QTableWidgetItem("200"))
            self.ui.dataTable.setItem(3, 0, QTableWidgetItem("1000"))
            self.ui.dataTable.setItem(4, 0, QTableWidgetItem("0"))

            # Second column dt
            self.ui.dataTable.setItem(0, 2, QTableWidgetItem("0.3"))
            self.ui.dataTable.setItem(1, 2, QTableWidgetItem("3.0"))
            self.ui.dataTable.setItem(2, 2, QTableWidgetItem("0.4"))
            self.ui.dataTable.setItem(3, 2, QTableWidgetItem("0.15"))
            self.ui.dataTable.setItem(4, 2, QTableWidgetItem("0.2"))

            # Third column n
            self.ui.dataTable.setItem(0, 1, QTableWidgetItem("7"))
            self.ui.dataTable.setItem(1, 1, QTableWidgetItem("14"))
            self.ui.dataTable.setItem(2, 1, QTableWidgetItem("7"))
            self.ui.dataTable.setItem(3, 1, QTableWidgetItem("14"))
            self.ui.dataTable.setItem(4, 1, QTableWidgetItem("0"))

            #Lock not needed cells
            item = self.ui.dataTable.item(self.ui.dataTable.rowCount()-1, 0)
            if item:
                item.setFlags(Qt.NoItemFlags)   # not selectable, not editable
                item.setText("Not Needed")
            
            item = self.ui.dataTable.item(self.ui.dataTable.rowCount()-1, 1)
            if item:
                item.setFlags(Qt.NoItemFlags)   # not selectable, not editable
                item.setText("Not Needed")

        elif data_type == "tilting_force":
            # Set horizontal header labels for tilting force, including Fa
            tilting_horizontal_labels = ["Fr (N)","Lr (m)", "Fa (N)","La (m)", "n (rpm)", "dt (s)"]
            tilting_vertical_labels = ["1","2", "3","max"]
            self.ui.dataTable.setColumnCount(len(tilting_horizontal_labels))
            self.ui.dataTable.setHorizontalHeaderLabels(tilting_horizontal_labels)
            self.ui.dataTable.setRowCount(len(tilting_vertical_labels))
            self.ui.dataTable.setVerticalHeaderLabels(tilting_vertical_labels)
            # First column Fr
            self.ui.dataTable.setItem(0, 0, QTableWidgetItem("400"))
            self.ui.dataTable.setItem(1, 0, QTableWidgetItem("320"))
            self.ui.dataTable.setItem(2, 0, QTableWidgetItem("200"))
            self.ui.dataTable.setItem(3, 0, QTableWidgetItem("1000"))
            # Second column Lr
            self.ui.dataTable.setItem(0, 1, QTableWidgetItem("0.2"))
            self.ui.dataTable.setItem(1, 1, QTableWidgetItem("0.2"))
            self.ui.dataTable.setItem(2, 1, QTableWidgetItem("0.2"))
            self.ui.dataTable.setItem(3, 1, QTableWidgetItem("0.2"))
            # Third column Fa
            self.ui.dataTable.setItem(0, 2, QTableWidgetItem("100"))
            self.ui.dataTable.setItem(1, 2, QTableWidgetItem("80"))
            self.ui.dataTable.setItem(2, 2, QTableWidgetItem("50"))
            self.ui.dataTable.setItem(3, 2, QTableWidgetItem("150"))
            # Fourth column La
            self.ui.dataTable.setItem(0, 3, QTableWidgetItem("1.5"))
            self.ui.dataTable.setItem(1, 3, QTableWidgetItem("1.5"))
            self.ui.dataTable.setItem(2, 3, QTableWidgetItem("1.5"))
            self.ui.dataTable.setItem(3, 3, QTableWidgetItem("1.5"))
            # Fifth column n
            self.ui.dataTable.setItem(0, 4, QTableWidgetItem("7"))
            self.ui.dataTable.setItem(1, 4, QTableWidgetItem("14"))
            self.ui.dataTable.setItem(2, 4, QTableWidgetItem("7"))
            self.ui.dataTable.setItem(3, 4, QTableWidgetItem("14"))
            # Sixth column dt
            self.ui.dataTable.setItem(0, 5, QTableWidgetItem("0.3"))
            self.ui.dataTable.setItem(1, 5, QTableWidgetItem("3.0"))
            self.ui.dataTable.setItem(2, 5, QTableWidgetItem("0.4"))
            self.ui.dataTable.setItem(3, 5, QTableWidgetItem("0.15"))

            


    def show_table(self):
        self.ui.dataTable.show()
        self.ui.file_path.hide()
        self.ui.label_2.hide()

    def show_file_path(self):
        self.ui.file_path.show()
        self.ui.dataTable.hide()
        self.ui.label_2.show()

    def insert_data(self):
        ''' 
        This function is called when the OK button is clicked
        it reads the data from the table and stores it in a 2D list of floats
        '''
        # initialize a 2D list to store the float data from the table
        self.float_data = [[0 for _ in range(self.ui.dataTable.columnCount())] for _ in range(self.ui.dataTable.rowCount())]
        
        if self.ui.array_s.isChecked():
            for col in range(self.ui.dataTable.columnCount()):
                for row in range(self.ui.dataTable.rowCount()):
                    #skip last row first two columns for lifetime and pause time
                    item = self.ui.dataTable.item(row, col)
                    flags = item.flags()
                    #skip un editable flags
                    if not (flags & Qt.ItemIsSelectable) and not (flags & Qt.ItemIsEditable):
                        continue
                    
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
        elif self.ui.json_s.isChecked():
            not_offered_dialog = NonNumbersDialog()
            not_offered_dialog.ui.textBrowser.setText("JSON input not yet supported")
            not_offered_dialog.exec_()
            return
        else:
            non_numbers_dialog = NonNumbersDialog()
            non_numbers_dialog.exec_()
            return
        
    def show_info(self):
        if self.data_type=="torque":
            torque_info_dialog = TorqueInfoDialog()
            torque_info_dialog.exec_()
        elif self.data_type=="tilting_force":
            force_info_dialog = ForceInfoDialog()
            force_info_dialog.exec_()

    def center_on_screen(self):
        frame_geometry = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())