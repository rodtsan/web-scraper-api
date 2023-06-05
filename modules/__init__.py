
# Import Libraries 
import os
import importlib

# Get all files.
files = [f for f in os.listdir(os.path.dirname(os.path.abspath(__file__))) if f.endswith(".py") and f != "__init__.py"]

# Import all files from modules folder.
for file in files:
    # print(os.path.dirname(os.path.realpath(__file__)).split('/')[-1])
    # importlib.import_module(os.path.dirname(os.path.realpath(__file__)).split('/')[-1] + "." + file[:-3])
    importlib.import_module("modules.{}".format(file[:-3]))
    


    
