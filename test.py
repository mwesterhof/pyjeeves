from jeeves import DBModel


class Person(DBModel):
    first_name = ''
    last_name = ''
    age = 0

    def __repr__(self):
        return '{0} {1} age {2}'.format(
            self.first_name,
            self.last_name,
            self.age
        )


class Test(DBModel):
    foo = 1
    bar = 2
    baz = ''

    def __repr__(self):
        return self.foo
