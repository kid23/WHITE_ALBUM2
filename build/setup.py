from distutils.core import setup
import py2exe


data = open("../output/dar.zip", "rb").read()

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': 1, 'optimize': 2, 'ascii': 1, 
    "dll_excludes": ["w9xpopen.exe"],
    "excludes": ["unittest"]}},
    zipfile = None,
    #author = 'KiD',
    #version = "1.0",
    console = [{
        'script': 'import_file.py',
        'other_resources': [(1,1,data)],
        #'icon_resources': [(1,'prog.ico')],
        },],
)

