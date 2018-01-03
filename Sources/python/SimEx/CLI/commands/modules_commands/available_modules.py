def process_args(args):
	show_available_modules()

def show_available_modules():
	from SimEx.CLI.utilities import parse_modules,parse_classes
	moduleList=parse_modules.get_available_modules()
	print("Available modules: ")
	print("="*88)
	print("%40s %20s %20s"%("Name","Class","Order"))
	print("="*88)
	for item in moduleList:
		print("%40s %20s %20s"% (item.get("Name"),item.get("Class"),
								parse_classes.get_class_priority(item.get("Class"))))
		print("-"*88)


if __name__ == "__main__":
	show_available_modules(None)
