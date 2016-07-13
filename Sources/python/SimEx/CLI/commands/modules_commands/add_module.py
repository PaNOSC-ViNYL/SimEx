from SimEx.CLI.utilities import parse_modules,parse_classes,parse_settings,project_files


def process_args(args):
	add_module(args.names)

def add_module(names):
	currentModules = parse_settings.get_all_modules()
	added  = False
	for name in names:
		if any(item['Name'] == name for item in parse_modules.get_available_modules()):
			if (name in currentModules):
				print "module %s is already added"%name
			else:
				currentModules.append(name)
				added  = True				
				print "adding module ",name
		else:
			print "Module %s not found"%name

	if (added): 
		currentModules = sorted(currentModules, key=lambda k: parse_modules.get_module_priority(k))
		parse_settings.set_settings('Modules',currentModules)
		project_files.update_main_file()	

if __name__ == "__main__":
	import sys
	add_module(sys.argv[1:])
	