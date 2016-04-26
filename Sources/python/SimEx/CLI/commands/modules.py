from modules_commands import add_module,available_modules,enable_module,list_modules,set_param


def set_arguments(parser):
    subparsers = parser.add_subparsers(title='module commands',help='')

# set parameter
    parser_set = subparsers.add_parser('set', help='set module parameter(s)')
    parser_set.set_defaults(func=set_param.process_args)
    parser_set.add_argument('name',metavar='<module name>',nargs=1,help='module name')
    parser_set.add_argument('parameters',metavar='<param=value>',nargs='+',help='module parameters')    
   

    
# add module
    parser_add = subparsers.add_parser('add', help='add module(s)')
    parser_add.set_defaults(func=add_module.process_args)

#enable module    
    parser_enable = subparsers.add_parser('enable', help='enable module(s)')
    parser_enable.set_defaults(func=enable_module.process_args_enable)
    
        
#disable module
    parser_disable = subparsers.add_parser('disable', help='disable module(s)')
    parser_disable.set_defaults(func=enable_module.process_args_disable)    
    
    for subparser in [parser_add, parser_enable, parser_disable]:
        subparser.add_argument('names',metavar='<module name>',nargs='+',help='module name')

# list project modules    
    parser_list = subparsers.add_parser('list', help='show project modules')
    parser_list.set_defaults(func=list_modules.process_args)

    
# list available modules    
    parser_avail = subparsers.add_parser('avail', help='show available modules')
    parser_avail.set_defaults(func=available_modules.process_args)


