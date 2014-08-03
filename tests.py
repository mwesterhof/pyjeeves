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

if __name__ == '__main__':
    unittest.main()
