import unittest
from test.Utils.db_decorator import client, atomic
from Models.models import Category


class TestCategories(unittest.TestCase):
    def insert_mock_data(self, session):
        category1 = Category(name="Category 1")
        category2 = Category(name="Category 2")
        session.add(category1)
        session.add(category2)
        session.commit()

    @atomic
    def test_create_category(self, session):
        response = client.post("/api/v1/categories/", json={"name": "Test Category"})
        self.assertEqual(response.status_code, 201)  # Cambié a 201 ya que se espera al crear un nuevo recurso
        data = response.json()
        self.assertEqual(data["name"], "Test Category")

    @atomic
    def test_get_category(self, session):
        self.insert_mock_data(session)
        response = client.get("/api/v1/categories/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Category 1")


if __name__ == '__main__':
    unittest.main()
