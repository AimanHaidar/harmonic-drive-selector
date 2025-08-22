from PyQt5 import QtWidgets
from gui.generated.first_selection_dialog import Ui_Dialog

class FirstSelectionDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.yes_button.clicked.connect(self.accept)
        self.ui.no_button.clicked.connect(self.reject)