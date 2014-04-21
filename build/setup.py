from distutils.core import setup
import os
import py2exe
import zipfile

def zip_dar(): 
    f = zipfile.ZipFile('../output/dar.zip','w',zipfile.ZIP_DEFLATED) 
    for dirpath, dirnames, filenames in os.walk('../output/dar/'): 
        for filename in filenames: 
            f.write(os.path.join(dirpath,filename), filename) 
    f.close() 

zip_dar()    
data = open("../output/dar.zip", "rb").read()
excludes = list()
for line in open("pylist.txt", "r").readlines():
    line=line.strip('\n')
    if (line.endswith('.pyo') or line.endswith('.pyd')):
        line = line[:-4]
    excludes.append(line)

setup(
    options = {'py2exe': 
                      {
                      'bundle_files': 1, 
                      'compressed': 1, 
                      'optimize': 2, 
                      'ascii': 1, 
                      'dll_excludes': ['w9xpopen.exe'],
                      "excludes": excludes
                      }
              },
    zipfile = None,
    #author = 'KiD',
    #version = "1.0",
    console = [{
        'script': 'import_file.py',
        'other_resources': [(1,1,data)],
        'icon_resources': [(1,'w6.ico')],
        },],
)

