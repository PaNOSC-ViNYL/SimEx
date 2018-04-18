from SimEx.CLI.utilities import parse_modules,parse_classes,parse_settings,project_files


def process_args_enable(args):
	enable_module(args.names,True)

def process_args_disable(args):
	enable_module(args.names,False)

def enable_module(names,enable):
	disabledModules = parse_settings.get_disabled_modules()
	enabledModules = parse_settings.get_modules()
	toEnable=[]
	toDisable=[]
	changed  = False
	for name in names:
		if any(item == name for item in disabledModules+enabledModules):
			if (name in enabledModules):
				if (enable):
					print("module %s is already enabled"%name)
				else:
					toDisable.append(name)
					changed  = True
					print("disabled module ",name)
			else:
				if (enable):
					toEnable.append(name)
					changed  = True
					print("enabled module ",name)
				else:
					print("module %s is already disabled"%name)
		else:
			print("Module %s not found"%name)

	if (changed):
		enabledModules += toEnable
		disabledModules += toDisable
		enabledModules = list(set(enabledModules) - set(toDisable))
		disabledModules = list(set(disabledModules) - set(toEnable))
		enabledModules = sorted(enabledModules, key=lambda k: parse_modules.get_module_priority(k))
		disabledModules = sorted(disabledModules, key=lambda k: parse_modules.get_module_priority(k))
		parse_settings.set_settings('Modules',enabledModules)
		parse_settings.set_settings('DisabledModules',disabledModules)
		project_files.update_main_file()

if __name__ == "__main__":
	import sys
	enable_module(sys.argv[1:],True)

