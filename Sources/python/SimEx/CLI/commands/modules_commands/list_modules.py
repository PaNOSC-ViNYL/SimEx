def process_args(args):
	show_project_modules()

def show_project_modules():
	from SimEx.CLI.utilities import parse_modules,parse_classes,parse_settings
	moduleList=parse_modules.get_available_modules()
	disabledModules = parse_settings.get_disabled_modules()
	enabledModules = parse_settings.get_modules()

	print "Project modules: "
	print "="*88
	print "%40s %20s %20s"%("Name","Class","Status")
	print "="*88
	for item in moduleList:
		if (item.get("Name") in disabledModules):
			status = "disabled"
		elif (item.get("Name") in enabledModules):
			status = "enabled"
		else:
			continue
		print "%40s %20s %20s"% (item.get("Name"),item.get("Class"),status)
		print "-"*88


if __name__ == "__main__":
	show_project_modules(None)
