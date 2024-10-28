from datetime import datetime
import inspect
import sqlite3


from hq import HeadQuarters


class Database:
    _hive_mind = {}

    def __init__(self, logging=False):
        # Borg design pattern
        self.__dict__ = self._hive_mind

        hq = HeadQuarters()
        self.name = hq.db_name

        self.db = sqlite3.connect(self.name)
        self.cursor = self.db.cursor()
        self.logging = logging

    def execute(self, command, logging=False):
        if self.logging or logging:
            print(command)
        try:
            self.cursor.execute(command)
        except Exception as e:
            print('{0}: {1}'.format(command, e))
            raise
        return self.cursor.fetchall()

    def _create_table(self, table_name, **fields):
        foreignkeys = []

        for key, value in fields.items():
            if value.startswith('relation_'):
                target_class = value.split('_', 1)[1]
                foreignkeys.append((key, target_class))
                fields[key] = 'INTEGER'

        fieldspec_list = [
            ' '.join([k, v])
            for k, v in fields.items()
        ] + [
            'pk INTEGER PRIMARY KEY'
        ]

        for fk in foreignkeys:
            fieldspec_list.append('FOREIGN KEY({0}) REFERENCES {1}(pk)'.format(
                fk[0],
                fk[1]
            ))
        self.execute(
            'CREATE TABLE IF NOT EXISTS {0} ({1})'.format(
                table_name,
                ', '.join(fieldspec_list)
            ),
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

    def _insert_into_table(self, table_name, **data):
        columns = '(' + ', '.join(data.keys()) + ')'
        values = '(' + ', '.join(
            [self._get_repr(val) for val in data.values()]
        ) + ')'

        self.execute('insert into {0} {1} values {2}'.format(
            table_name,
            columns,
            values
        ))
        self.db.commit()
        result = self.execute('SELECT pk FROM {0} WHERE rowid={1}'.format(
            table_name,
            self.cursor.lastrowid
        ))
        return result[0][0]

    def _update_in_table(self, table_name, **data):
        pk = data.pop('pk')

        columns_expression = ', '.join(
            [
                '='.join([key, self._get_repr(value)])
                for key, value in data.items()
            ]
        )

        self.execute('UPDATE {0} SET {1} WHERE pk={2}'.format(
            table_name,
            columns_expression,
            pk
        ))
        self.db.commit()

    def _delete_from_table(self, table_name, pk):
        self.execute('DELETE FROM {0} WHERE pk={1}'.format(
            table_name,
            pk
        ))
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
        data = obj.__dict__.copy()

        for k, v in data.items():
            if v.__class__.__class__ == DBModelMeta:
                data[k] = v.pk
            elif v.__class__ == datetime:
                data[k] = v.isoformat()

        return self._insert_into_table(name, **data)

    def delete_object(self, obj):
        name = obj.__class__.__name__.lower()
        return self._delete_from_table(name, obj.pk)


class DBModelMeta(type):
    def __new__(cls, name, bases, dict_):
        def sql_type(val):
            t = type(val)
            if t == datetime:
                return 'DATETIME'
            if t in [str]:
                return 'TEXT'
            if t == int:
                return 'INTEGER'
            if t == DBModelMeta:
                return 'relation_' + val.get_table_name()
            # fallback
            return 'TEXT'

        if name != 'DBModel':
            fields = dict([
                (f, sql_type(val))
                for f, val in dict_.items()
                if not f.startswith('_')
            ])
            Database().register(name, fields)
        return super(DBModelMeta, cls).__new__(cls, name, bases, dict_)


class DBModel(metaclass=DBModelMeta):
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

        keys_to_pop = []
        for k, v in kwargs.items():
            if not v and not k == 'pk':
                keys_to_pop.append(k)
                continue

            # TODO: methinks we need lazy loading here,
            # instead of preloading
            if k in default and default[k].__class__ == DBModelMeta:
                try:
                    kwargs[k] = default[k].find(pk=kwargs[k].pk)[0]
                except AttributeError:
                    kwargs[k] = default[k].find(pk=kwargs[k])[0]

        for key in keys_to_pop:
            kwargs.pop(key)

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
        if self.pk and self.find(pk=self.pk):
            return Database().update_object(self)
        else:
            self.pk = Database().insert_object(self)

    def delete(self):
        if self.pk:
            return Database().delete_object(self)
