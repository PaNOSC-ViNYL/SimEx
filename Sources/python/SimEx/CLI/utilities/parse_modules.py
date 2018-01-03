import json
import sys
import os

import SimEx.Calculators
from . import parse_classes

def get_module_from_file(fname):
    f=open(fname,'r')
    moduleDescription = json.load(f)
    moduleDescription["Simex Module"] = True
    f.close()
    return moduleDescription



def get_available_modules():
    from . import parse_classes
    path = os.path.dirname(SimEx.Calculators.__file__)+'/RegisteredCalculators/'
    moduleList=[]
    for fname in os.listdir(path):
            if not '_ParamTemplate.py' in fname:
                moduleList.append(get_module_from_file(path+fname))
    moduleList = sorted(moduleList, key=lambda k: parse_classes.get_class_priority(k['Class']))
    return moduleList

def get_module_priority(moduleName):
    moduleList = get_available_modules()
    for item in moduleList:
        if item.get("Name") == moduleName and item.get("Class"):
            return parse_classes.get_class_priority(item["Class"])
    return None

def get_module(moduleName):
    moduleList = get_available_modules()
    for item in moduleList:
        if item.get("Name") == moduleName:
            return item
    return None


if __name__ == "__main__":
        print(get_available_modules())
