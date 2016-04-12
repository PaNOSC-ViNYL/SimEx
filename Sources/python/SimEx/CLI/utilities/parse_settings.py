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
           raise Exception() 
    except:
        print ("Cannot open open or corrupted file: %s"%fname)
        sys.exit(1)


def get_project_name():
    return get_settings('Project Name')