'''
This module demonstrates the use of the DBModel base class. By simply creating
your own subclass, you instruct the database layer to create an appropriate
table for it. Any values defined in the class will correspond to a column, its
type will be matched to the value type in the class, and the actual value will
be used as a default, if we attempt to save the object without specifying that
value.
'''

from database import DBModel


# the name of our class and (lowercased) table
class Person(DBModel):
    # the table should contain a column called "first_name"
    # datatype CHAR, default value ""
    first_name = ''

    # the same for "last_name"
    last_name = ''

    # and also an INT called "age"
    age = 0

    # we can define methods and properties as we please
    # this just makes "print <person object>" print a nice formatted string
    def __repr__(self):
        return '{0} {1} age {2}'.format(
            self.first_name,
            self.last_name,
            self.age
        )


# and we can make as many classes as we like
class Test(DBModel):
    test_int = 1
    person_link = Person

person = Person()
person.save()
Test(person_link=person).save()
