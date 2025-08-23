from PyQt5 import QtWidgets
from gui.generated.non_numbers_dialog import Ui_Dialog

class NonNumbersDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)
