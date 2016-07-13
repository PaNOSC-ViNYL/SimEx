import json
import sys
import os

import SimEx.Calculators

def get_class(fname):
    f=open(fname,'r')
    moduleClass = json.load(f)
    f.close()
    return moduleClass

def get_available_classes():
    path = os.path.dirname(SimEx.Calculators.__file__)+'/CalculatorClasses/'
    classList=[]
    for fname in os.listdir(path):
            classList.append(get_class(path+fname))
    return classList

def get_class_priority(className):
    classList = get_available_classes()
    for item in classList:
        if item.get("Class Name") == className and item.get("Order"):
            return int(item["Order"])
    return None

if __name__ == "__main__":
        print get_available_classes()
        