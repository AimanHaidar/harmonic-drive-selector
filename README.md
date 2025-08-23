# Harmonic Drive Selector
This is a Harmonic Drive app build with qt5 allow engineers to easly select the appropriat drive for thier application by inpouting tourqe and angular speed data for thier load

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
    - using directly the main.py
    ```bash
    uv run main.py
    ```

    - building the project and get one exeutable file using pyinstaller

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

    it will create dist folder contain the executable






