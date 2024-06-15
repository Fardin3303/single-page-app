import unittest
from datetime import datetime
from sqlalchemy import create_engine
import sys
import os
from sqlmodel import SQLModel, Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.models import User, PointOfInterest
from unit_tests.db_config import SQLALCHEMY_DATABASE_URL

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SQLModel.metadata.create_all(cls.engine)
    
    @classmethod
    def tearDownClass(cls):
        SQLModel.metadata.drop_all(cls.engine)

    def setUp(self):
        self.session = Session(self.engine)
    
    def test_create_user(self):
        user = User(username="testuser", hashed_password="hashed_password")
        self.session.add(user)
        self.session.commit()

        retrieved_user = self.session.get(User, user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.hashed_password, "hashed_password")

    def test_create_point_of_interest(self):
        user = User(username="testuser2", hashed_password="hashed_password")
        self.session.add(user)
        self.session.commit()

        poi = PointOfInterest(
            description="Test POI",
            latitude="12.34",
            longitude="56.78",
            created_at=datetime.now(),
            user_id=user.id
        )
        self.session.add(poi)
        self.session.commit()

        retrieved_poi = self.session.get(PointOfInterest, poi.id)
        self.assertIsNotNone(retrieved_poi)
        self.assertEqual(retrieved_poi.description, "Test POI")
        self.assertEqual(retrieved_poi.latitude, "12.34")
        self.assertEqual(retrieved_poi.longitude, "56.78")
        self.assertEqual(retrieved_poi.user_id, user.id)

    def test_relationship(self):
        user = User(username="testuser3", hashed_password="hashed_password")
        poi = PointOfInterest(
            description="Test POI",
            latitude="12.34",
            longitude="56.78",
            created_at=datetime.now()
        )
        user.points_of_interest.append(poi)
        
        poi2 = PointOfInterest(
            description="Test POI 2",
            latitude="12.34",
            longitude="56.78",
            created_at=datetime.now()
        )
        user.points_of_interest.append(poi2)
        self.session.add(user)
        self.session.commit()



        retrieved_user = self.session.get(User, user.id)
        self.assertEqual(len(retrieved_user.points_of_interest), 2)
        self.assertEqual(retrieved_user.points_of_interest[0].description, "Test POI")

if __name__ == "__main__":
    unittest.main()