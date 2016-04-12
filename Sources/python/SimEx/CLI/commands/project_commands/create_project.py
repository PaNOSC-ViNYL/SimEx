
import json
import shutil

def process_args(args):
	create_project(args.name)

def create_project(name):
	import os,sys,fileinput
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
		f.write(json.dumps(d))
		f.close()
	except OSError:
		print "Cannot create project, remove directory .simex"
		return	
	
	src = os.path.dirname(__file__)+"/../../../Templates/main.py"
	dest= fname+'.py'
	try:	
		if os.path.exists(dest):
			raise IOError("Destination file exists!")
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

if __name__ == "__main__":
	import sys
	create_project(sys.argv[1])