PYJeeves
========
__work in progress__

This project should eventually implement various database-backed tricks and shortcuts, to streamline human-computer interaction in a terminal environment.

As it stands, it currently implements a high-level database wrapper, tailored to an SQLite backend.

DONE
-----
* Support automatic primary keys (and update vs insert)
* full CRUD
* respect default values in db models
* testsuite (basic)
* model.save(), model should have pk

DOING
-----
* better testing for relations
    * fix id on save

TODO
----
want:
    relations:
        * query
        * Reverse relations

* Plugin system
* Further tools

optional:

* Support other SQL backends
