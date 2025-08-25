from PyQt5 import QtWidgets
from gui.generated.input_lifetime_dialog import Ui_Dialog
from gui.dialogs.non_numbers_dialog import NonNumbersDialog
from PyQt5.QtCore import QTimer

class InputLifetimeDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        QTimer.singleShot(0, self.center_on_screen)
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

    def center_on_screen(self):
        frame_geometry = self.frameGeometry()
        screen = QtWidgets.QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())