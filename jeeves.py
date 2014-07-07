import sqlite3

from os import path

root_dir = path.dirname(__file__)


class Database(object):
    _hive_mind = {}

    def __init__(self, name=path.join(root_dir, 'jeeves.db'), logging=False):
        # Borg design pattern
        self.__dict__ = self._hive_mind

        self.db = sqlite3.connect(name)
        self.cursor = self.db.cursor()
        self.logging = logging

    def execute(self, command, logging=False):
        if self.logging or logging:
            print command
        self.cursor.execute(command)
        return self.cursor.fetchall()
        
    def _create_table(self, name, **fields):
        layout = '(' + ', '.join(
                [' '.join([n, type_])
                for n, type_ in fields.items()]
                ) + ')'

        self.execute(
                'create table if not exists {0} {1}'.format(name, layout),
        )
        self.db.commit()

    def _insert_into_table(self, name, **data):
        columns = '(' + ', '.join(data.keys()) + ')'
        values = '(' + ', '.join([repr(val) for val in data.values()]) + ')'

        self.execute('insert into {0} {1} values {2}'.format(name, columns, values), logging=True)
        self.db.commit()

    def _listing(self, name, *fields):
        if not fields:
            fields = '*'
        else:
            fields = ', '.join(fields)

        return self.execute(
                'select {0} from {1}'.format(fields, name)
        )

    def register(self, name, fields):
        return self._create_table(
                name.lower(), **fields
        )

    def save_objects(self, objects):
        for obj in objects:
            print obj.__dict__
            name = obj.__class__.__name__.lower()
            data = obj.__dict__
            return self._insert_into_table(name, **data)


class DBModelMeta(type):
    def __new__(cls, name, bases, dict_):
        def sql_type(val):
            t = type(val)
            if t in [str, unicode]:
                return 'text'
            if t == int:
                return 'int'

            # fallback
            return 'text'

        if name != 'DBModel':
            fields = dict([
                (f, sql_type(val))
                for f, val in dict_.items()
                if not f.startswith('_')
            ])
            Database().register(name, fields)
        return super(DBModelMeta, cls).__new__(cls, name, bases, dict_)


class DBModel(object):
    __metaclass__ = DBModelMeta

    def save(self):
        return Database().save_objects([self])

