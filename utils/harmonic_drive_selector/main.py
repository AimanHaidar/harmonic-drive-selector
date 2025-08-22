import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets
from gui.src.mainwindow import Ui_MainWindow
from gui.src.about import Ui_Form
import sys
from pathlib import Path

# Add data to path
sys.path.append(str(Path(__file__).resolve().parent)+"/src")
sys.path.append(str(Path(__file__).resolve().parent)+"/gui")

class HarmonicSelctorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        #self.exper_ui.setupUi(self)
        # connect pushButton to a function
        self.ui.about_pushButton.clicked.connect(self.show_about)

    def show_about(self):
        # This function is called when the start button is clicked
        self.Form = QtWidgets.QWidget()
        self.about = Ui_Form()
        self.about.setupUi(self.Form)
        self.Form.show()

def main():
    print("Hello from harmonic-drives-selector!")
    app = QApplication(sys.argv)
    window = HarmonicSelctorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
