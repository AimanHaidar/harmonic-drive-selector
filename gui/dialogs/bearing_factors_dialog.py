from PyQt5 import QtWidgets
from gui.generated.bearing_factor_dialog import Ui_Dialog

class BearingFactorsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)