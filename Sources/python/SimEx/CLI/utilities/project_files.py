import shutil
import os,sys,fileinput

import SimEx,parse_settings,parse_modules

def copy_module_parameters(moduleName):
    module = parse_modules.get_module(moduleName)
    path = os.path.dirname(SimEx.Calculators.__file__)+'/RegisteredCalculators/'
    src = path + moduleName + "_ParamTemplate.py"
    dest = moduleName+"_params.py"
    shutil.copy(src,dest)
    
def create_modulecall_code(moduleName,prevModule,nextModule):
    module = parse_modules.get_module(moduleName)
    print moduleName,prevModule,nextModule

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
    if (modules == None): return
    
    for i,module in enumerate(modules):
        copy_module_parameters(module)
        next = modules[i+1] if i < len(modules)-1 else None
        prev = modules[i-1] if i > 0 else None
        create_modulecall_code(module,prev,next)
        
        