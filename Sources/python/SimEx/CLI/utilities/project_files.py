import shutil
import os,sys,fileinput

import SimEx,parse_settings

def update_main_file():
    
    fname = parse_settings.get_project_name()
    src = os.path.dirname(SimEx.__file__)+"/Templates/main.py"
    dest= fname+'.py'
    try:    
        if os.path.exists(dest):
            bakfile=dest.replace('.py','.bak')
            shutil.copy(dest,bakfile)
            print ("Overwriting file %s, file %s created"%(dest,bakfile))
        shutil.copy(src,dest)
        for line in fileinput.FileInput(dest, inplace=1):
            line=line.replace('${PROJECT_NAME}',fname)
            print line.strip()        
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e)
    except :
        print('Error: cannot create file %s'%dest )        
        return
    modules = parse_settings.get_modules()
    if (len(modules)):
        print aaa