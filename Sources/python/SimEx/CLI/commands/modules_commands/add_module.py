def process_args(args):
	add_module(args.names)

def add_module(names):
	print "adding module " ,names

if __name__ == "__main__":
	import sys
	add_module(sys.argv[1:])