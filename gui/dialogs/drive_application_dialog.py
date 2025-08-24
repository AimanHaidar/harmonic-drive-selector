from PyQt5 import QtWidgets
from gui.generated.drive_application_dialog import Ui_Dialog

class DriveApplicationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
