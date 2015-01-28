import glob
import os
import sys


def get_doc_for_plugin(path):
    old_spath = sys.path
    sys.path.append(os.path.dirname(path))
    plugin = __import__(os.path.basename(path).split('.')[0])
    sys.path = old_spath
    return (plugin.Plugin.__doc__ or '').strip()


def get_plugins():
    folder_main = os.path.join(os.path.dirname(__file__), 'plugins')
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


class BasePlugin(object):
    dependencies = []

    def run_command(self, args):
        raise NotImplementedError('run_command')
