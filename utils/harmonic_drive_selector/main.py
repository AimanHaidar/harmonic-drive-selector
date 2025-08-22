import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from gui.generated.mainwindow import Ui_MainWindow
from gui.generated.about import Ui_Form

from gui.dialogs.first_selection_dialog import FirstSelectionDialog
from gui.dialogs.cable_dialog import CableDialog
from gui.dialogs.selection_input_dialog import SelectionInputDialog

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

    def start_selection(self):
        first_selection_dialog = FirstSelectionDialog()
        first_selection = first_selection_dialog.exec_()
        if  first_selection == first_selection_dialog.Accepted:
            cable_dialog = CableDialog()
            cable_dialog.exec_()
        
        elif first_selection == first_selection_dialog.Rejected:
            selection_input_dialog = SelectionInputDialog()
            selection_input_dialog.exec_()


    def show_about(self):
        # This function is called when the start button is clicked
        self.Form = QtWidgets.QWidget()
        self.about = Ui_Form()
        self.about.setupUi(self.Form)
        self.Form.show()

def main():
    print("Hello from harmonic-drives-selector!")
    app = QApplication(sys.argv)
    window = HarmonicSelctorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
