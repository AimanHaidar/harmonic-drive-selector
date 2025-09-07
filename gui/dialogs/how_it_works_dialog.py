from PyQt5 import QtWidgets
from gui.generated.how_it_works_dialog import Ui_Dialog
from PyQt5.QtCore import Qt

class HowItWorksDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(
            Qt.Window |
            Qt.WindowMinimizeButtonHint|
            Qt.WindowMaximizeButtonHint|
            Qt.WindowCloseButtonHint
            )
        self.showMaximized()
