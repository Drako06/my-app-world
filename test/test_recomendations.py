import unittest
from test.Utils.db_decorator import client, atomic
from Models.models import Location, Category, LocationCategoryReviewed
from datetime import datetime, timedelta


class TestRecommendations(unittest.TestCase):
    def insert_mock_data(self, session):
        location1 = Location(name="Location 1", latitude=10.0, longitude=20.0)
        location2 = Location(name="Location 2", latitude=30.0, longitude=40.0)
        session.add(location1)
        session.add(location2)

        category1 = Category(name="Category 1")
        category2 = Category(name="Category 2")
        session.add(category1)
        session.add(category2)

        review1 = LocationCategoryReviewed(location_id=1, category_id=1,
                                           last_reviewed=(datetime.now() - timedelta(days=31)).isoformat())
        review2 = LocationCategoryReviewed(location_id=2, category_id=2,
                                           last_reviewed=(datetime.now() - timedelta(days=31)).isoformat())
        session.add(review1)
        session.add(review2)

        session.commit()

    @atomic
    def test_get_recommendations(self, session):
        self.insert_mock_data(session)
        response = client.get("/api/v1/recommendations/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(len(data) <= 10)
        for item in data:
            self.assertTrue(
                datetime.strptime(item["last_reviewed"], "%Y-%m-%dT%H:%M:%S.%f") < datetime.utcnow() - timedelta(
                    days=30))


if __name__ == '__main__':
    unittest.main()
