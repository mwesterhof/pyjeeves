import os

from plugin import BasePlugin


class Plugin(BasePlugin):
    '''
    Initialize an HQ in the current directory
    '''
    def run_command(self, args):
        print 'creating jeeves headquarters in {0}'.format(os.getcwd())
        os.makedirs('.jeeves')
