
import json
import os

import create_project 


def process_args(args):
	create_test_project()

def prGreen(prt,newline=True):
	if (newline):
		print("\033[92m{}\033[00m" .format(prt))
	else:
		print("\033[92m{}\033[00m" .format(prt)),
	
def prCyan(prt,newline=True):
	if (newline):
		print("\033[96m{}\033[00m" .format(prt))
	else:
		print("\033[96m{}\033[00m" .format(prt)),


def runCommented(cmd,comment):
	prCyan('*'*80)
	prCyan(comment+':')
	prGreen(cmd)
	prCyan('*'*80)	
	os.system(cmd)


def create_test_project():
	if os.listdir('.'):
		print('Cannot create test project, directory is not empty') 
		return

	modules_to_test = ["XFELPhotonSource","XFELPhotonPropagator","XMDYNDemoPhotonMatterInteractor",
					   "SingFELPhotonDiffractor","PerfectPhotonDetector","S2EReconstruction"]
	
	filestocopy = ["$SIMEX_TESTS/python/unittest/TestFiles/s2e.*","$SIMEX_TESTS/python/unittest/TestFiles/sample.h5",
				   "$SIMEX_TESTS/python/unittest/TestFiles/FELsource_out.h5"]
	
	commands = [
				["create project","simex project create test"],
				["print available modules","simex module avail"],
				["add modules to the project","simex module add "+' '.join(modules_to_test)],
				["print project modules","simex module list"],
				["make input dir and copy necessary files (not simex command)",
					"mkdir -p input/FELsource && cp "+ ' '.join(filestocopy)+" input" + \
					" && mv input/FELsource_out.h5 input/FELsource"],
				["set module parameter","simex module set XFELPhotonSource input_path=input/FELsource"],
				["set another module parameter","simex module set S2EReconstruction EMC_Parameters:max_number_of_iterations=2"],
			   ]
	
	for cmd in commands:
		runCommented(cmd[1],cmd[0])
		
	prCyan("Type",False),prGreen("simex run",False),prCyan("to start simulations")	
	
if __name__ == "__main__":
	import sys
	create_test_project()