from project_commands import create_project,create_test_project


def set_arguments(parser):
    subparsers = parser.add_subparsers(title='project commands',help='')
    parser = subparsers.add_parser('create', help='create project')
    parser.add_argument('name',metavar='<name>',nargs=1,help='Project name')
    parser.set_defaults(func=create_project.process_args)
    parser = subparsers.add_parser('create-test', help='create test project')
    parser.set_defaults(func=create_test_project.process_args)


