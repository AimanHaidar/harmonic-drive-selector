import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from gui.generated.mainwindow import Ui_MainWindow
from gui.generated.about import Ui_Form

from gui.dialogs.first_selection_dialog import FirstSelectionDialog
from gui.dialogs.cable_dialog import CableDialog
from gui.dialogs.selection_input_dialog import SelectionInputDialog
from gui.dialogs.type_inform_dialog import TypeInformDialog
from gui.dialogs.data_dialog import DataDialog

import sys
from pathlib import Path

# Add data to path
sys.path.append(str(Path(__file__).resolve().parent)+"/src")
sys.path.append(str(Path(__file__).resolve().parent)+"/gui")

class HarmonicSelctorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #self.exper_ui.setupUi(self)
        # connect pushButton to a function
        self.ui.about_pushButton.clicked.connect(self.show_about)
        self.ui.start_pushButton.clicked.connect(self.start_selection)
        self.ui.exit_pushButton.clicked.connect(self.close)

    def start_selection(self):
        first_selection_dialog = FirstSelectionDialog()
        first_selection = first_selection_dialog.exec_()
        if  first_selection == first_selection_dialog.Rejected:
            cable_dialog = CableDialog()
            with_cable = cable_dialog.exec_()
            if with_cable == cable_dialog.Accepted:
                self.infrom_type("SHG. ")
            else:
                self.infrom_type("CSG. ")

            if not self.informed:
                return
        
        elif first_selection == first_selection_dialog.Accepted:
            selection_input_dialog = SelectionInputDialog()
            selection_input_dialog.exec_()
            self.first_selection = selection_input_dialog.ui.lineEdit.text()
            print(self.first_selection)
            
        self.input_data()

    def show_about(self):
        # This function is called when the start button is clicked
        self.Form = QtWidgets.QWidget()
        self.about = Ui_Form()
        self.about.setupUi(self.Form)
        self.Form.show()
    
    def input_data(self):
        data_dialog = DataDialog()
        data_dialog.exec_()
        return data_dialog.ui.dataTable.item

    def infrom_type(self,type):
        type_inform_dialog = TypeInformDialog()
        type_inform_dialog.ui.harmonic_type.setText(type)
        self.informed = type_inform_dialog.exec_()

def main():
    print("Hello from harmonic-drives-selector!")
    app = QApplication(sys.argv)
    window = HarmonicSelctorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
