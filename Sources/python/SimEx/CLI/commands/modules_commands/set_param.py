from SimEx.CLI.utilities import parse_modules,parse_classes,parse_settings,module_files
import os

def process_args(args):
	set_parameters(args.name,args.parameters)

def getFromDict(dataDict, mapList):
	try:
		vals = reduce(lambda d, k: d[k], mapList, dataDict)
	except:
		raise Exception		
	return vals


def setInDict(dataDict, mapList, value):
	old_value = getFromDict(dataDict, mapList) # to check if parameter exists
	getFromDict(dataDict, mapList[:-1])[mapList[-1]] = type(old_value)(value)

def set_param(param,module):
	try:
		key,value=param.split("=")
		if (key == 'input_path'):
			module.input_path=value
			return True
		elif (key == 'output_path'):
			module.output_path=value
			return True				
		keys=key.split(':')
		setInDict(module.parameters,keys,value)
		return True
	except:
		print ("Cannot set %s. Wrong parameter"%param)
		return False

def set_parameters(name,params):
	name=str(name[0])
	enabledModules = parse_settings.get_modules()
	if (name not in enabledModules):
		print "Module %s not found"%name
		return

	paramfile = name+'_params'
	
	module = __import__(paramfile)
	
	picfile = name+'_params.pyc'
	os.remove(picfile)


	to_write = False
	for param in params:
		ok = set_param(param,module)
		if ok == True:
			to_write=True
		
	if (to_write):
		module_files.write_module_parameters(name,module)
	
	
if __name__ == "__main__":
	import sys
	set_param(sys.argv[1:])
	