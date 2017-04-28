
import json
import os

from SimEx.CLI.utilities.project_files import update_main_file


def process_args(args):
	create_project(args.name)

def create_project(name):
	try:
		fname=str(name[0])
		open(fname,'w').close()
		os.unlink(fname)
	except OSError:
		print('Project name is not valid.')
		return

	try:
		os.mkdir(".simex")
		d = {'Project Name': fname}
		f=open('.simex/settings','w')
		f.write(json.dumps(d,indent=4))
		f.close()
	except OSError:
		print "Cannot create project, remove directory .simex"
		return

	update_main_file()


if __name__ == "__main__":
	import sys
	create_project(sys.argv[1])
