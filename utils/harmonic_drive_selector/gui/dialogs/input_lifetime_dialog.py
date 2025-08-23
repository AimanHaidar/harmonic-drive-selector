from PyQt5 import QtWidgets
from gui.generated.input_lifetime_dialog import Ui_Dialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog

class InputLifetimeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.check_input)
        self.ui.buttonBox.rejected.connect(self.reject)

    def check_input(self):
        item = self.ui.lineEdit.text()
        if item is None or item == "":
            non_numbers_dialog = NonNumbersDialog()
            non_numbers_dialog.exec_()
            return
        try:
            self.lifetime = float(item)
        except ValueError:
            non_numbers_dialog = NonNumbersDialog()
            non_numbers_dialog.exec_()
            return
        self.accept()