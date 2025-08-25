import sys

from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox
from PyQt5 import QtWidgets, QtGui
from gui.generated.mainwindow import Ui_MainWindow
from gui.generated.about import Ui_Form
from gui.dialogs.first_selection_dialog import FirstSelectionDialog
from gui.dialogs.cable_dialog import CableDialog
from gui.dialogs.selection_input_dialog import SelectionInputDialog
from gui.dialogs.type_inform_dialog import TypeInformDialog
from gui.dialogs.data_dialog import DataDialog
from gui.dialogs.input_lifetime_dialog import InputLifetimeDialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog
from gui.dialogs.result_dialog import ResultDialog
from gui.dialogs.drive_application_dialog import DriveApplicationDialog
from gui.dialogs.bearing_factors_dialog import BearingFactorsDialog

from src.harmonic_dasigner import torque_based_dimensioning,stiffness_based_dimensioning,output_bearing_dimensioning
from data.reducers_tables import reducers_df

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
        ''' This function is called when the start button is clicked 
        it opens a dialog to select the type of harmonic drive and then opens
        the data input dialog and then the lifetime input dialog and finally shows the result dialog
        for the Data
        '''
        # create dialog it ask user if he had selected a harmonic drive before or not
        first_selection_dialog = FirstSelectionDialog()
        first_selection = first_selection_dialog.exec_()
        if first_selection == first_selection_dialog.Rejected:
            return
        #this boolean to know if the user selected a harmonic drive
        #to determine how to input to torque_based_dimensioning function
        first_selection_mode = False
        #to know weather  the user push yes or no in first selection dialog
        if  first_selection_dialog.answer == False:
            #ask user if he want to select SHG or CSG
            #if yes SHG if no CSG
            cable_dialog = CableDialog()
            with_cable = cable_dialog.exec_()
            # if the user closed the dialog or pushed cancel close the selection process
            if with_cable == cable_dialog.Rejected:
                return
            if cable_dialog.answer == True:
                self.type = "SHG"
                #use the infrom_type that generate dialog to inform the user with his selection
                self.infrom_type("you choosed SHG.do you want to proceed selecting with this type?")
            else:
                self.type = "CSG"
                self.infrom_type("you choosed CSG.do you want to proceed selecting with this type?")

            #from infrom_type function we get if the user accepted or rejected
            if not self.informed:
                return
        
        # if the user selected yes in first selection dialog
        elif first_selection_dialog.answer == True:
            #dialog for user to  input the first selection
            selection_input_dialog = SelectionInputDialog()
            state = selection_input_dialog.exec_()
            try:
                #get the first selection from the dialog
                self.first_selection = selection_input_dialog.first_selection
                first_selection_mode = True
            except AttributeError:
                pass
            # if the user closed the dialog or pushed cancel close the selection process
            if selection_input_dialog.Rejected == state:
                return
        # get the data from the data dialog
        self.torque_data = self.input_data("torque")
        #close selection process if no data is input is cancelled
        if not self.torque_data:
            return
        # Combine T and n into one load_data dictionary
        self.load_data = {
            'T_cycle': [self.torque_data[0][0], self.torque_data[1][0], self.torque_data[2][0]],
            'T_k': self.torque_data[3][0],
            't_k': self.torque_data[3][2],
            't_p': self.torque_data[4][2],
            'dt': [self.torque_data[0][2], self.torque_data[1][2], self.torque_data[2][2]],
            'n_cycle': [self.torque_data[0][1], self.torque_data[1][1], self.torque_data[2][1]],
            'n_k': self.torque_data[3][1]
        }

        #dialog to input the required lifetime of the harmonic drive
        input_lifetime_dialog = InputLifetimeDialog()
        state = input_lifetime_dialog.exec_()
        #close if user cancelled
        if state == input_lifetime_dialog.Rejected:
            return
        self.lifetime = input_lifetime_dialog.lifetime
        if first_selection_mode:
            #do the selection based on the first selection
            #run selection algorithm
            self.selection1 = torque_based_dimensioning(
                self.first_selection['Series'],
                self.load_data,
                self.lifetime,
                self.first_selection
            )

        else:
            #do the selection based on the type only
            self.selection1 = torque_based_dimensioning(
                self.type,
                self.load_data,
                self.lifetime
            )
        
        self.show_result(self.selection1)

        if self.continue_dimensioning:
            #open the drive application dialog to get the type of application
            drive_application_dialog = DriveApplicationDialog()
            state = drive_application_dialog.exec_()
            if state == drive_application_dialog.Rejected:
                return
            application_type = drive_application_dialog.ui.application_type.currentText()
            load_moment_of_inertia_dialog = InputLifetimeDialog()
            load_moment_of_inertia_dialog.ui.label.setText("your load moment of inertia:")
            state = load_moment_of_inertia_dialog.exec_()
            if state == load_moment_of_inertia_dialog.Rejected:
                return
            load_moment_of_inertia = load_moment_of_inertia_dialog.lifetime

            self.selection2 = stiffness_based_dimensioning(self.selection1,application_type,load_moment_of_inertia)
            self.selection2 = torque_based_dimensioning(self.selection2.split("-")[0],
                self.load_data,
                self.lifetime,
                first_selection = {
                "Series":self.selection2.split("-")[0],
                "Size":int(self.selection2.split("-")[1]),
                "Ratio":int(self.selection2.split("-")[2])
                }
                )
            self.show_result(self.selection2)

            if self.continue_dimensioning:
                #TODO add bearing factors dialog here and edit the data dialog to input F_tilting
                self.tilting_force_data = self.input_data("tilting_force")
                if not self.tilting_force_data:
                    return
                # Combine tilting force data into one dictionary
                self.tilting_data = {
                    'Fr_cycle': [self.tilting_force_data[0][0], self.tilting_force_data[1][0], self.tilting_force_data[2][0]],
                    'Lr_cycle': [self.tilting_force_data[0][1], self.tilting_force_data[1][1], self.tilting_force_data[2][1]],
                    'Fa_cycle': [self.tilting_force_data[0][2], self.tilting_force_data[1][2], self.tilting_force_data[2][2]],
                    'La_cycle': [self.tilting_force_data[0][3], self.tilting_force_data[1][3], self.tilting_force_data[2][3]],
                    'dt': [self.tilting_force_data[0][5], self.tilting_force_data[1][5], self.tilting_force_data[2][5]],
                    'R': self.tilting_force_data[3][1],
                    'Fr_max': self.tilting_force_data[3][0],
                    'Lr_max': self.tilting_force_data[3][1],
                    'Fa_max': self.tilting_force_data[3][2],
                    'La_max': self.tilting_force_data[3][3],
                    'n_cycle': [self.tilting_force_data[0][4], self.tilting_force_data[1][4], self.tilting_force_data[2][4]],
                    't_p': self.tilting_force_data[3][2]
                }
                print(self.tilting_data)
                bearing_factors_dialog = BearingFactorsDialog()
                state = bearing_factors_dialog.exec_()
                if state == bearing_factors_dialog.Rejected:
                    return
                self.selection3 = output_bearing_dimensioning(self.selection2,self.tilting_data,bearing_factors_dialog.operating_factor,bearing_factors_dialog.minimum_static_safety_factor,20000)
                self.selection3 = torque_based_dimensioning(self.selection3.split("-")[0],
                    self.load_data,
                    self.lifetime,
                    first_selection = {
                    "Series":self.selection3.split("-")[0],
                    "Size":int(self.selection3.split("-")[1]),
                    "Ratio":int(self.selection3.split("-")[2])
                    }
                )
                self.show_result(self.selection3,last=True)

            


            

    def show_about(self):
        '''This function is called when the about button in mainwindow is clicked '''
        self.Form = QtWidgets.QWidget()
        self.about = Ui_Form()
        self.about.setupUi(self.Form)
        self.Form.show()
    
    def input_data(self,data_type="torque"):
        '''This function opens the data input dialog and returns the data as a list of lists
        Parameters:
            data_type: str, type of data to input, can be "torque" or "tilting force"

        Returns:
            list of data or False if dialog is cancelled
        '''
        data_dialog = DataDialog(data_type)
        state = data_dialog.exec_()
        if state == data_dialog.Accepted:
            return data_dialog.float_data
        else:
            return False

    def infrom_type(self,type):
        type_inform_dialog = TypeInformDialog()
        type_inform_dialog.ui.harmonic_type.setText(type)
        self.informed = type_inform_dialog.exec_()

    def show_result(self,selection,last=False):
        
        print(selection)
        drive_specs = reducers_df[(reducers_df["Series"] == selection.split("-")[0]) & (reducers_df["Size"] == int(selection.split("-")[1])) & (reducers_df["Ratio"] == int(selection.split("-")[2]))]
        drive_specs = drive_specs.to_numpy().transpose()
        result_dialog = ResultDialog()
        if last:
            result_dialog.ui.label_3.hide()
        result_dialog.fill_table(result_dialog.data_model,result_dialog.ui.dataTableView,self.torque_data)
        result_dialog.fill_table(result_dialog.specs_model,result_dialog.ui.driveTableView,drive_specs)
        result_dialog.ui.selection.setText((selection))
        if selection.split("-")[0] in ["HFUC","CSG"]:
            result_dialog.ui.drive_photo.setPixmap(QtGui.QPixmap(":/pictures/pictures/CSG_photo.png"))
        else:
            result_dialog.ui.drive_photo.setPixmap(QtGui.QPixmap(":/pictures/pictures/SHG_photo.png"))
        self.continue_dimensioning = (result_dialog.exec_() == result_dialog.Accepted)

def show_exception_box(exc_type, exc_value, exc_traceback):
    """Show only the exception message in a QMessageBox (no details)."""
    QMessageBox.critical(None, "Error", str(exc_value))

# Install handler
#sys.excepthook = show_exception_box

def main():
    print("Hello from harmonic-drives-selector!")
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = HarmonicSelctorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
