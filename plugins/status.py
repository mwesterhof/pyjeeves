import sys

from hq import HeadQuarters, JeevesError
from plugin import BasePlugin, get_plugins


class Plugin(BasePlugin):
    '''
    Show the status
    '''
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
