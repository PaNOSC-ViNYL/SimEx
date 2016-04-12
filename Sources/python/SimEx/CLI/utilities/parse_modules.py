import json
import sys
import os

import SimEx.Calculators
import parse_classes


def get_module(fname):
    f=open(fname,'r')
    moduleDescription = json.load(f)
    f.close()
    return moduleDescription

def get_available_modules():
    import parse_classes
    path = os.path.dirname(SimEx.Calculators.__file__)+'/RegisteredCalculators/'
    moduleList=[]
    for fname in os.listdir(path):
            if not '_ParamTemplate.py' in fname:
                moduleList.append(get_module(path+fname))
    moduleList = sorted(moduleList, key=lambda k: parse_classes.get_class_priority(k['Class']))                 
    return moduleList

def get_module_priority(moduleName):
    moduleList = get_available_modules()
    for item in moduleList:
        if item.get("Name") == moduleName and item.get("Class"):
            return parse_classes.get_class_priority(item["Class"])
    return None

if __name__ == "__main__":
        print get_available_modules()
        