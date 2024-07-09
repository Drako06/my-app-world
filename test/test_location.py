import unittest
from test.Utils.db_decorator import client, atomic
from Models.models import Location


class TestLocations(unittest.TestCase):
    def insert_mock_data(self, session):
        location1 = Location(name="Location 1", latitude=10.0, longitude=20.0)
        location2 = Location(name="Location 2", latitude=30.0, longitude=40.0)
        session.add(location1)
        session.add(location2)
        session.commit()

    @atomic
    def test_create_location(self, session):
        response = client.post("/api/v1/locations/", json={"name": "Test Location", "latitude": 10.0, "longitude": 20.0})
        self.assertEqual(response.status_code, 201)  # Cambié a 201 ya que se espera al crear un nuevo recurso
        data = response.json()
        self.assertEqual(data["name"], "Test Location")
        self.assertEqual(data["latitude"], 10.0)
        self.assertEqual(data["longitude"], 20.0)

    @atomic
    def test_get_location(self, session):
        self.insert_mock_data(session)
        response = client.get("/api/v1/locations/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Location 1")
        self.assertEqual(data["latitude"], 10.0)
        self.assertEqual(data["longitude"], 20.0)


if __name__ == '__main__':
    unittest.main()
