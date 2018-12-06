from os import unlink

from hq import HeadQuarters
from plugin import BasePlugin


class Plugin(BasePlugin):
    '''
    Removes the database file from the current HQ
    '''
    def run_command(self, args):
        hq = HeadQuarters()
        print('cleaning up database in {0}'.format(hq.hq))
        try:
            unlink(hq.db_name)
        except OSError:
            pass
