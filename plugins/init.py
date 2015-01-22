import os


def run_command(args):
    print 'creating jeeves headquarters in {0}'.format(os.getcwd())
    os.makedirs('.jeeves')
