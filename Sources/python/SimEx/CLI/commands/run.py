from utilities.parse_settings import get_project_name

def set_arguments(parser):
    parser.set_defaults(func=run)

def run(args):
    import os    
    command='python ./'+get_project_name()+'.py'
    os.system(command)
    
if __name__ == "__main__":
    import sys
    run(None)    