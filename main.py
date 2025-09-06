
from gui.harmonic_selector_app import HarmonicSelctorApp
from gui.harmonic_selector_app import apply_global_style
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets

def main():
    print("Hello from harmonic-drives-selector!")
    app = QApplication(sys.argv)
    apply_global_style(app)
    window = HarmonicSelctorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
