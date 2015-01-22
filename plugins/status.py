from hq import HeadQuarters


def run_command(args):
    hq = HeadQuarters()
    print 'Jeeves status:'
    print 'headquarters @{0}'.format(hq.hq)
