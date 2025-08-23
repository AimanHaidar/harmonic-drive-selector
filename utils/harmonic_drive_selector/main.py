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
from gui.dialogs.input_lifetime_dialog import InputLifetimeDialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog

from src.harmonic_dasigner import tourqe_based_dimensioning

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
        proceed = True
        if  first_selection == first_selection_dialog.Rejected:
            cable_dialog = CableDialog()
            with_cable = cable_dialog.exec_()
            if with_cable == cable_dialog.Accepted:
                self.type = "SHG"
                self.infrom_type("SHG. ")
            else:
                self.type = "CSG"
                self.infrom_type("CSG. ")

            if not self.informed:
                return
        
        elif first_selection == first_selection_dialog.Accepted:
            selection_input_dialog = SelectionInputDialog()
            state = selection_input_dialog.exec_()
            try:
                self.first_selection = selection_input_dialog.first_selection
            except AttributeError:
                pass
            if selection_input_dialog.Rejected == state:
                proceed = False

        if proceed:
            self.data = self.input_data()
            if not self.data:
                return
            self.T = {}
            self.T = {}
            self.T['T_cycle'] = [self.data[0][0], self.data[1][0], self.data[2][0]]
            self.T['T_k']     = self.data[3][0]
            self.T['t_k']     = self.data[3][2]
            self.T['t_p']     = self.data[4][2]
            self.T['dt'] = [self.data[0][2], self.data[1][2], self.data[2][2]]

            self.n = {}
            self.n['n_cycle'] = [self.data[0][1], self.data[1][1], self.data[2][1]]
            self.n['n_k']     = self.data[3][1]


            input_lifetime_dialog = InputLifetimeDialog()
            state = input_lifetime_dialog.exec_()
            if state == input_lifetime_dialog.Rejected:
                return
            self.lifetime = input_lifetime_dialog.lifetime

            print(tourqe_based_dimensioning(self.first_selection['Series'],self.T,self.n,self.lifetime,self.first_selection))


    def show_about(self):
        # This function is called when the start button is clicked
        self.Form = QtWidgets.QWidget()
        self.about = Ui_Form()
        self.about.setupUi(self.Form)
        self.Form.show()
    
    def input_data(self):
        data_dialog = DataDialog()
        state = data_dialog.exec_()
        if state == data_dialog.Accepted:
            return data_dialog.float_data
        else:
            return False

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
