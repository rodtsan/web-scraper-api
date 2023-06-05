# Import Libraries
import os
import importlib

# Get all linkedin api files.
files = pyfiles = [
    f
    for f in os.listdir(os.path.dirname(os.path.abspath(__file__)))
    if f.endswith(".py") and f != "__init__.py"
]

# Import all files from modules folder.
for file in pyfiles:
    importlib.import_module("modules.linkedin.{}".format(file[:-3]))
