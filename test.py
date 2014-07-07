from jeeves import DBModel


class Foo(DBModel):
    foo = 0
    bar = 0
    baz = 0


class Bar(DBModel):
    foo = ''


bla = Foo()
bla.foo = 1
bla.bar = 2
bla.baz = 3
bla.save()
