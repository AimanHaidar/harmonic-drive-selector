# Harmonic Drive Selector
This is a Harmonic Drive app built with Qt5 that allows engineers to easily select the appropriate drive for their application by inputting torque and angular speed data for their load.

## Screenshots
![Description of image](screenshots/main_window.png)

## Installation

1. **Clone the repository**  

```bash
git clone https://github.com/AimanHaidair/harmonic-drive-selector.git
cd harmonic-drive-selector
```

2. **sync uv project**

```bash
uv sync
```

3. **now you have two options to run:**
    - **option 1:** using directly the main.py
    ```bash
    uv run main.py
    ```

    - **option 2:** building the project and get one exeutable file using pyinstaller

        1. install pyinstall in your vevn

        ```bash
            uv add pyinstall
        ```
        2. run this command

            ##### Linux:
            ```bash
            .venv/bin/python -m PyInstaller --onefile main.py
            ```

            ##### Windows:
            ```powershell
            .venv\Scripts\python.exe -m PyInstaller --onefile --windowed main.py
            ```

        this will create dist folder contain the executable






