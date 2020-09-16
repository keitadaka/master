from cx_Freeze import setup, Executable

base = None    

executables = [Executable("Appli_Synchro.py", base=base)]

packages = ["idna", "tkinter", "os", "shutil", "stat", "datetime"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Appli Synchro",
    options = options,
    version = "1.0",
    description = 'Application de synchonisation elaboré par Daka KEITA, Date : 07/2020',
    executables = executables
)

