from project_commands import create_project


def set_arguments(parser):
    subparsers = parser.add_subparsers(title='project commands',help='')
    parser = subparsers.add_parser('create', help='create project')
    parser.add_argument('name',metavar='<name>',nargs=1,help='Project name')
    parser.set_defaults(func=create_project.process_args)


