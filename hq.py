import os


class JeevesError(Exception):
    pass


class HeadQuarters(object):
    def __init__(self):
        hq = self.get_hq()

        self.hq = hq
        self.db_name = os.path.join(hq, 'database')

    def get_hq(self):
        old_cwd = None
        cwd = os.getcwd()

        hq = os.path.join(cwd, '.jeeves')
        while not os.path.exists(hq):
            if old_cwd == cwd:
                return self.get_home_hq()
            old_cwd = cwd
            cwd = os.path.dirname(cwd)
        return os.path.join(cwd, '.jeeves')

    def get_home_hq(self):
        return os.path.expanduser(os.path.join('~', '.pyjeeves'))


if __name__ == '__main__':
    hq = HeadQuarters()
    print(hq.hq)
