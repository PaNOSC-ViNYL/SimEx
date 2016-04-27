import shutil
import os,sys,fileinput

import SimEx,parse_settings,parse_modules
import pprint
   
def write_module_parameters(moduleName,module):
    dest= moduleName+'_params.py'
    try:
        if os.path.exists(dest):
            bakfile=dest.replace('.py','.bak')
            shutil.copy(dest,bakfile)
            print ("Overwriting file %s, file %s created"%(dest,bakfile))
    except IOError as e:
        print('Error: %s' % e)
    except :
        print('Error: cannot create file %s'%dest )        
        return
    modfile = open(dest, 'w')

    print>>modfile, 'input_path  = ',repr(module.input_path),'\n'
    print>>modfile, 'output_path  = ',repr(module.output_path),'\n'
    s=pprint.pformat(module.parameters)
    print>>modfile,'parameters = ',s
    
    modfile.close()
    
    
