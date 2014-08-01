import inspect
from os import path
import sqlite3


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
        layout = '(' + \
            ', '.join(
                [' '.join([n, type_])
                    for n, type_ in fields.items()] +
                ['pk INTEGER PRIMARY KEY']
            ) + ')'

        self.execute(
            'create table if not exists {0} {1}'.format(name, layout),
        )
        self.db.commit()

    def query(self, cls, lookup):
        name = cls.get_table_name()
        lookup_parts = [
            '{0}={1}'.format(k, repr(v))
            for k, v in lookup.items()
        ]
        lookup = ' and '.join(lookup_parts)
        if lookup:
            lookup = ' where ' + lookup
        results = self.execute('select * from {0}{1}'.format(name, lookup))
        columns = [item[0] for item in self.cursor.description]
        data = [dict(zip(columns, item)) for item in results]
        return [cls(**item) for item in data]

    def _get_repr(self, value):
        if value is None:
            return 'NULL'
        return repr(value)

    def _insert_into_table(self, name, **data):
        columns = '(' + ', '.join(data.keys()) + ')'
        values = '(' + ', '.join(
            [self._get_repr(val) for val in data.values()]
        ) + ')'

        self.execute('insert into {0} {1} values {2}'.format(
            name,
            columns,
            values
        ), logging=True)
        self.db.commit()

    def _update_in_table(self, name, **data):
        pk = data.pop('pk')

        columns_expression = ', '.join(
            [
                '='.join([key, self._get_repr(value)])
                for key, value in data.iteritems()
            ]
        )

        self.execute('UPDATE {0} SET {1} WHERE pk={2}'.format(
            name,
            columns_expression,
            pk
        ), logging=True)
        self.db.commit()

    def _delete_from_table(self, name, pk):
        self.execute('DELETE FROM {0} WHERE pk={1}'.format(
            name,
            pk
        ), logging=True)
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

    def update_object(self, obj):
        name = obj.__class__.__name__.lower()
        data = obj.__dict__
        return self._update_in_table(name, **data)

    def insert_object(self, obj):
        name = obj.__class__.__name__.lower()
        data = obj.__dict__
        return self._insert_into_table(name, **data)

    def delete_object(self, obj):
        name = obj.__class__.__name__.lower()
        return self._delete_from_table(name, obj.pk)


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

    def __init__(self, **kwargs):
        super(DBModel, self).__init__()

        default = dict([
            m
            for m in inspect.getmembers(self)
            if not (
                m[0].startswith('_') or
                inspect.ismethod(m[1]) or
                m[0] == 'pk'
            )
        ])
        self.__dict__.update(default)

        for k, v in kwargs.items():
            if not v and not k == 'pk':
                kwargs.pop(k)
        self.pk = None
        self.__dict__.update(kwargs)

    @classmethod
    def find(cls, **lookup):
        results = Database().query(cls, lookup)
        return results

    @classmethod
    def get_table_name(cls):
        return cls.__name__.lower()

    def save(self):
        if self.pk and not self.find(pk=self.pk):
            return Database().update_object(self)
        else:
            return Database().insert_object(self)

    def delete(self):
        if self.pk:
            return Database().delete_object(self)
