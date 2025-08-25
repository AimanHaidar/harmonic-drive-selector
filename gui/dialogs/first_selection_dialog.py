from PyQt5 import QtWidgets
from gui.generated.first_selection_dialog import Ui_Dialog

class FirstSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.yes_button.clicked.connect(self.yes)
        self.ui.no_button.clicked.connect(self.no)

    def yes(self):
        self.answer = True
        self.accept()
        
    def no(self):
        self.answer = False
        self.accept()  
