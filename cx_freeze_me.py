from cx_Freeze import setup, Executable

setup(
    name = "StepMania Songs to Sheet",
    version = "1.0",
    description = "StepMania Songs to Sheet",
    executables = [Executable("songs_to_sheet.py")]
)
