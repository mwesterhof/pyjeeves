class BasePlugin(object):
    def run_command(self, args):
        raise NotImplementedError('run_command')
