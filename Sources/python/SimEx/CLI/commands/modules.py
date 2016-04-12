from modules_commands import add_module


def set_arguments(parser):
    subparsers = parser.add_subparsers(title='modules commands',help='')
    parser = subparsers.add_parser('add', help='add module(s)')
    parser.add_argument('names',metavar='module',nargs='+',help='module name')
    parser.set_defaults(func=add_module.process_args)


