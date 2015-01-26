import os

from plugin import BasePlugin


class Plugin(BasePlugin):
    def run_command(self, args):
        print 'creating jeeves headquarters in {0}'.format(os.getcwd())
        os.makedirs('.jeeves')
