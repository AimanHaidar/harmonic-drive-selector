from PyQt5 import QtWidgets
from gui.generated.cable_dialog import Ui_Dialog

class CableDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
