import shutil
import os,sys,fileinput

import SimEx,parse_settings,parse_modules

def copy_module_parameters(moduleName):
    module = parse_modules.get_module(moduleName)
    path = os.path.dirname(SimEx.Calculators.__file__)+'/RegisteredCalculators/'
    src = path + moduleName + "_ParamTemplate.py"
    dest = moduleName+"_params.py"
    if not os.path.exists(dest):
        shutil.copy(src,dest)

def create_modulecall_code(moduleName,prevModule,nextModule):
    module = parse_modules.get_module(moduleName)
    codelines = """

#======================================================================================
# Module ${ModuleName}
#======================================================================================

from SimEx.Calculators.${ModuleName} import ${ModuleName}
import ${ModuleName}_params

if (${ModuleName}_params.output_path == 'default'):
    ${ModuleName}_params.output_path = "output/${ModuleName}"
    if not os.path.exists('output'): os.makedirs('output')

${SetInputToPrevModulePath}

${ModuleName}_inst = ${ModuleName} (
                                    parameters=${ModuleName}_params.parameters,
                                    input_path=${ModuleName}_params.input_path,
                                    output_path=${ModuleName}_params.output_path
                                    )
prCyan("-"*80)
prCyan ("Running ${ModuleName} ...")
module_time=time.time()
${ModuleName}_inst.backengine()
prCyan ("Done in "+str(datetime.timedelta(seconds=time.time()-module_time)))
                       """
    prevpath = """
if (${ModuleName}_params.input_path == 'default'):
    ${ModuleName}_params.input_path = "output/${PrevModuleName}"
               """
    if (prevModule):
        codelines=codelines.replace("${SetInputToPrevModulePath}",prevpath)
        codelines=codelines.replace("${PrevModuleName}",prevModule)
    else:
        codelines=codelines.replace("${SetInputToPrevModulePath}","")
    codelines=codelines.replace("${ModuleName}",moduleName)

    return codelines

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
            print line.rstrip()
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e)
    except :
        print('Error: cannot create file %s'%dest )
        return

    modules = parse_settings.get_modules()
    if (modules == []): return

    string=''
    for i,module in enumerate(modules):
        copy_module_parameters(module)
        next = modules[i+1] if i < len(modules)-1 else None
        prev = modules[i-1] if i > 0 else None
        string+=create_modulecall_code(module,prev,next)

    for line in fileinput.FileInput(dest, inplace=1):
            line=line.replace('# modules will be added here',string)
            print line.rstrip()
