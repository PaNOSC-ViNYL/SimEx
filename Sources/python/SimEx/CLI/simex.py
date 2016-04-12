#! /usr/bin/env python

import argparse
from commands import modules,project,run

parser = argparse.ArgumentParser(prog='simex')

subparsers = parser.add_subparsers(title='simex commands',help='')

parser_project = subparsers.add_parser('project', help='project related commands')
project.set_arguments(parser_project)

parser_modules = subparsers.add_parser('modules', help='modules related commands')
modules.set_arguments(parser_modules)

parser_run     = subparsers.add_parser('run', help='run simex')
run.set_arguments(parser_run)

args = parser.parse_args()
args.func(args)