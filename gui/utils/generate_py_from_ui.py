import os
import subprocess
from pathlib import Path

# base project root (one level up from utils/)
BASE_DIR = Path(__file__).resolve().parent.parent  

UI_DIR = BASE_DIR / "ui"                # ui/ folder at project root
OUT_DIR = BASE_DIR / "generated"  # gui/generated/ folder

OUT_DIR.mkdir(parents=True, exist_ok=True)

for ui_file in UI_DIR.glob("*.ui"):
    py_file = OUT_DIR / f"{ui_file.stem}.py"
    cmd = ["pyuic5", "-o", str(py_file), str(ui_file)]
    print("Converting:", ui_file.name, "->", py_file.name)
    subprocess.run(cmd, check=True)

    if ui_file.name == "mainwindow.ui" or ui_file.name == "result_dialog.ui":
        file_path = str(OUT_DIR / ui_file.name).replace(".ui", ".py")
        with open(file_path, "r") as file:
            lines = file.readlines()
        with open(file_path, "w") as file:
            for line in lines:
                if line.strip() == "import pic_rc":
                    file.write("from ..resources import pic_rc\n")
                else:
                    file.write(line)

