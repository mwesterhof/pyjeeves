import glob
import os
import sys

from hq import HeadQuarters, JeevesError


def get_plugins():
    folder_main = os.path.dirname(__file__)
    folder_home = os.path.expanduser(os.path.join('~', '.pyjeeves', 'plugins'))

    results = set()

    for folder in [folder_main, folder_home]:
        search = os.path.join(folder, '*.py')
        print search
        n = set(glob.glob(search))
        results |= n

    results = [os.path.basename(p).split('.')[0] for p in results]
    return sorted(results)


def run_command(args):
    plugins = get_plugins()

    try:
        hq = HeadQuarters()
        print 'Jeeves status:'
        print 'headquarters @{0}'.format(hq.hq)
        print 'plugins:'
        for plugin in plugins:
            print '\t', plugin
    except JeevesError:
        sys.exit('No headquarters found. Create using the "init" plugin')
