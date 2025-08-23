from PyQt5 import QtWidgets
from gui.generated.selection_input_dialog import Ui_Dialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog
from data.reducers_tables import reducers_df
import re

pattern = re.compile(r'^(CSG|SHG)-\d+-\d+-2UH$')
class SelectionInputDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.disconnect()
        self.ui.buttonBox.accepted.connect(self.check_input)
        self.ui.buttonBox.rejected.connect(self.reject)

    def check_input(self):
        input = self.ui.lineEdit.text()
        print(input)
        if bool(pattern.match(input)):
            first_selection = input.split("-")
            try:
                result = reducers_df[(reducers_df["Series"] == first_selection[0]) & (reducers_df["Size"] == int(first_selection[1])) & (reducers_df["Ratio"] == int(first_selection[2]))]
                first_index = (result.index.values[0])
                self.first_selection = {'Series': first_selection[0],'Size': int(first_selection[1]),'Ratio': int(first_selection[2])}
            except Exception as e:
                non_numbers_dialog = NonNumbersDialog()
                non_numbers_dialog.exec_()
                return
        else:
            non_numbers_dialog = NonNumbersDialog()
            non_numbers_dialog.exec_()
            return
        self.accept()