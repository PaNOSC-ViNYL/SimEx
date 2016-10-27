import json
import sys

def get_settings(key):
    try:
        fname = '.simex/settings'
        f=open(fname,'r')
        settings = json.load(f)
        if key in settings.keys():
            return settings[key]
        else:
           return None 
    except:
        print ("Cannot open open or corrupted file: %s"%fname)
        sys.exit(1)


def get_project_name():
    return get_settings('Project Name')

def get_all_modules():
    return get_modules() + get_disabled_modules()

def get_modules():
    list = get_settings('Modules')
    if (list == None):
        return []
    else:
        return list

def get_disabled_modules():
    list = get_settings('DisabledModules')
    if (list == None):
        return []
    else:
        return list
    

def set_settings(key,value):
    try:
        fname = '.simex/settings'
        f=open(fname,'r')
        settings = json.load(f)
        f.close()
        settings[key] = value
        f=open(fname,'w')
        f.write(json.dumps(settings,indent=4))
        f.close()
    except:
        print ("Cannot set value in file: %s"%fname)
        sys.exit(1)
