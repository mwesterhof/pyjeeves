import glob
import os
import sys

from hq import HeadQuarters, JeevesError
from plugin import BasePlugin


def get_doc_for_plugin(path):
    old_spath = sys.path
    sys.path.append(os.path.dirname(path))
    plugin = __import__(os.path.basename(path).split('.')[0])
    sys.path = old_spath
    return (plugin.Plugin.__doc__ or '').strip()


def get_plugins():
    folder_main = os.path.dirname(__file__)
    folder_home = os.path.expanduser(os.path.join('~', '.pyjeeves', 'plugins'))

    results = set()

    for folder in [folder_main, folder_home]:
        search = os.path.join(folder, '*.py')
        n = set(glob.glob(search))
        results |= n

    combined = [
        (os.path.basename(result).split('.')[0], get_doc_for_plugin(result))
        for result in results
    ]

    return sorted(combined, key=lambda i: i[0])


class Plugin(BasePlugin):
    def run_command(self, args):
        plugins = get_plugins()

        try:
            hq = HeadQuarters()
            print 'Jeeves status:'
            print 'headquarters @{0}'.format(hq.hq)
            print 'plugins:'
            for plugin in plugins:
                print '\t', plugin[0]
                if plugin[1]:
                    print '\t' * 2, plugin[1]
        except JeevesError:
            sys.exit('No headquarters found. Create using the "init" plugin')
