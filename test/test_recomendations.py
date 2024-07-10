import unittest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from main import app
from Models.models import Location, Category, LocationCategoryReviewed
from Schemas.schemas import LocationCreate, CategoryCreate
from db.db_config import SessionLocal, get_db
from test.Utils.db_decorator import override_get_db, atomic

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db


class TestReadRecommendations(unittest.TestCase):

    @atomic
    def create_test_data(self, session):
        # Crear ubicaciones y categorías de prueba
        location1 = Location(name="Test Location 1", latitude=12.34, longitude=56.78)
        location2 = Location(name="Test Location 2", latitude=98.76, longitude=54.32)
        category1 = Category(name="Test Category 1")
        category2 = Category(name="Test Category 2")

        session.add(location1)
        session.add(location2)
        session.add(category1)
        session.add(category2)
        session.commit()

        # Crear revisiones de ubicación-categoría de prueba
        reviewed1 = LocationCategoryReviewed(location_id=location1.id, category_id=category1.id,
                                             last_reviewed=datetime.now() - timedelta(days=31))
        reviewed2 = LocationCategoryReviewed(location_id=location2.id, category_id=category2.id, last_reviewed=None)

        session.add(reviewed1)
        session.add(reviewed2)
        session.commit()

    @atomic
    def test_read_recommendations(self, session):
        # Crear datos de prueba
        self.create_test_data(session=session)

        # Hacer la solicitud al endpoint
        response = client.get("/recommendations/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("response", response.json())
        self.assertIsInstance(response.json()["response"], list)
        self.assertGreater(len(response.json()["response"]), 0)

        # Verificar que las primeras combinaciones no hayan sido revisadas
        for recommendation in response.json()["response"]:
            self.assertIn("location", recommendation)
            self.assertIn("category", recommendation)


if __name__ == "__main__":
    unittest.main()