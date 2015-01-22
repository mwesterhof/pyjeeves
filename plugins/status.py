import sys

from hq import HeadQuarters, JeevesError


def run_command(args):
    try:
        hq = HeadQuarters()
        print 'Jeeves status:'
        print 'headquarters @{0}'.format(hq.hq)
    except JeevesError:
        sys.exit('No headquarters found. Create using the "init" plugin')
