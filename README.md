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

TODO
---------
* better testing for relations
    * fix id on save
    * query

DOING
-----
* Reverse relations

TODO
----
want:

* Plugin system
* Further tools

optional:

* Support other SQL backends
