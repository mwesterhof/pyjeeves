from os import unlink

from hq import HeadQuarters


def run_command(args):
    hq = HeadQuarters()
    print 'cleaning up database in {0}'.format(hq.hq)
    try:
        unlink(hq.db_name)
    except OSError:
        pass
