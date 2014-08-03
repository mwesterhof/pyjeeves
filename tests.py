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
        obj.save()

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

        results = TestUpdateModel.find()
        self.assertEqual(len(results), 1)

        obj = results[0]
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


if __name__ == '__main__':
    unittest.main()
