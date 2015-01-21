from os import path, unlink
import unittest

from jeeves import Database, DBModel


class JeevesTest(unittest.TestCase):
    def setUp(self):
        Database('/tmp/jeeves.db')

    def tearDown(self):
        unlink('/tmp/jeeves.db')

    def test_create(self):
        class TestCreateModel(DBModel):
            foo = 1
            bar = 2
            baz = ''

        self.assertFalse(TestCreateModel.find())

        obj = TestCreateModel()
        self.assertFalse(obj.pk)
        obj.save()
        self.assertTrue(obj.pk)

        self.assertTrue(TestCreateModel.find())

    def test_retrieve(self):
        class TestRetrieveModel(DBModel):
            foo = 1
            bar = 2
            baz = ''

        TestRetrieveModel(foo=2).save()
        self.assertEqual(TestRetrieveModel.find()[0].foo, 2)

    def test_update(self):
        class TestUpdateModel(DBModel):
            foo = 1
            bar = 2
            baz = ''

        obj = TestUpdateModel()
        obj.save()

        self.assertEqual(obj.foo, 1)

        obj.foo = 2
        obj.save()
        self.assertEqual(TestUpdateModel.find()[0].foo, 2)

    def test_delete(self):
        class TestDeleteModel(DBModel):
            foo = 1
            bar = 2
            baz = ''

        TestDeleteModel().save()
        results = TestDeleteModel.find()
        self.assertEqual(len(results), 1)

        results[0].delete()
        results = TestDeleteModel.find()
        self.assertEqual(len(results), 0)

    def test_full_crud_galore(self):
        class TestModelA(DBModel):
            foo = 0

        class TestModelB(DBModel):
            foo = ''

        TestModelA().save()
        for i in range(1, 6):
            TestModelA(foo=i).save()
        self.assertEqual(TestModelA.find()[3].foo, 3)

    def test_basic_relationals(self):
        class FooModel(DBModel):
            name = ''

        class BarModel(DBModel):
            foo_link = FooModel

        foo = FooModel(name='baz')
        foo.save()

        bar = BarModel(foo_link=foo)
        bar.save()

        self.assertEqual(bar.foo_link.name, 'baz')
        bar.foo_link.name = 'baz1'
        bar.foo_link.save()

        self.assertEqual(bar.foo_link.name, 'baz1')

        # this part should be enabled once relational lookups work
        # foo = FooModel.find(parent=bar)
        # self.assertEqual(foo.name, 'baz1')

    def test_reverse_lookup(self):
        class ParentModel(DBModel):
            pass

        class ChildModel(DBModel):
            parent = ParentModel

        parent = ParentModel()
        parent.save()

        child = ChildModel(parent=parent)
        child.save()

        self.assertEqual(ChildModel.find()[0].parent.pk, parent.pk)
if __name__ == '__main__':
    unittest.main()
