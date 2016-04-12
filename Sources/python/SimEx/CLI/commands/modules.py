from modules_commands import add_module,available_modules


def set_arguments(parser):
    subparsers = parser.add_subparsers(title='module commands',help='')
    parser = subparsers.add_parser('add', help='add module(s)')
    parser.add_argument('names',metavar='module',nargs='+',help='module name')
    parser.set_defaults(func=add_module.process_args)
    
    parser = subparsers.add_parser('avail', help='show available modules')
    parser.set_defaults(func=available_modules.process_args)


