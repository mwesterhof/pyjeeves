#!/usr/bin/python

from os import path
import sys


if len(sys.argv) < 2:
    sys.argv.append('status')


args = sys.argv[1:]
plugin_name = args.pop(0)

jeeves_rootpath = path.dirname(path.realpath(__file__))

old_path = sys.path
sys.path.extend([
    jeeves_rootpath,
    path.expanduser(path.join('~', '.pyjeeves', 'plugins')),
    path.join(jeeves_rootpath, 'plugins')
])
plugin = __import__(plugin_name)
sys.path = old_path

plugin.Plugin().run_command(args)
