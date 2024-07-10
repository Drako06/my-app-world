import unittest
from test.Utils.db_decorator import client, atomic
#from Models.models import Category


class TestCategories(unittest.TestCase):

    @atomic
    def test_create_category(self, session):
        response = client.post("/api/v1/categories/", json={"name": "Test Category"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Category")



if __name__ == '__main__':
    unittest.main()
