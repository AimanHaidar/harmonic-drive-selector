from PyQt5 import QtWidgets
from gui.generated.bearing_factors_dialog import Ui_Dialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog

class BearingFactorsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.load_condition.currentTextChanged.connect(self.appropriate_factors)
        self.minimum_static_safety_factor = 1.5
        self.ui.operating_cond_bearing.currentTextChanged.connect(self.appropriate_factors)
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.check_input)
        self.ui.buttonBox.rejected.connect(self.reject)

    def appropriate_factors(self):
        load_condition = self.ui.load_condition.currentText()
        if load_condition == "No impact loads or vibrations":
            self.ui.operating_factor_range.setText("recommended operating factor: 1.0 - 1.2")
        elif load_condition == "Normal loads":
            self.ui.operating_factor_range.setText("recommended operating factor: 1.2 - 1.5")
        elif load_condition == "Impact loads or vibrations":
            self.ui.operating_factor_range.setText("recommended operating factor: 1.5 - 3.0")

        bearing_operating_condition = self.ui.operating_cond_bearing.currentText()
        if bearing_operating_condition == "Normal operating conditions":
            self.minimum_static_safety_factor = 1.5
        elif bearing_operating_condition == "In case vibrations or impacts":
            self.minimum_static_safety_factor = 2.0
        elif bearing_operating_condition == "For the highest demands on transmission accuracy":
            self.minimum_static_safety_factor = 3.0
    
    def check_input(self):
        item = self.ui.operating_factor.text()
        if item is None or item == "":
            non_numbers_dialog = NonNumbersDialog()
            non_numbers_dialog.exec_()
            return
        try:
            self.operating_factor = float(item)
        except ValueError:
            non_numbers_dialog = NonNumbersDialog()
            non_numbers_dialog.exec_()
            return
        self.accept()
        
            