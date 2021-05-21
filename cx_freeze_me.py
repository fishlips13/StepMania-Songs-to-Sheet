from cx_Freeze import setup, Executable

build_exe_options = {
    "build_exe" : "build/Songs to Sheet",
    "excludes": ["tkinter"]
    }

setup(
    name = "StepMania Songs to Sheet",
    version = "1.0",
    description = "StepMania Songs to Sheet",
    executables = [Executable("songs_to_sheet.py", target_name="Songs to Sheet.exe")],
    options = {"build_exe": build_exe_options}
)