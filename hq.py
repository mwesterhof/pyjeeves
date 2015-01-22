import os


class JeevesError(Exception):
    pass


class HeadQuarters(object):
    def __init__(self):
        old_cwd = None
        cwd = os.getcwd()

        hq = os.path.join(cwd, '.jeeves')
        while not os.path.exists(hq):
            if old_cwd == cwd:
                raise JeevesError('hq not found')
            old_cwd = cwd
            cwd = os.path.dirname(cwd)
            hq = os.path.join(cwd, '.jeeves')

        self.hq = hq
        self.db_name = os.path.join(hq, 'database')


if __name__ == '__main__':
    hq = HeadQuarters()
    print hq.hq
