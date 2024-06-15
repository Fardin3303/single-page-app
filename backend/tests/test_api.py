import unittest
import requests


class TestAPI(unittest.TestCase):
    BASE_URL = "http://0.0.0.0:8000"


    def create_user(self, username, password):
        response = requests.post(
            f"{self.BASE_URL}/users/",
            json={"username": username, "password": password},
            headers={"accept": "application/json", "Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    def request_token(self, username, password):
        response = requests.post(
            f"{self.BASE_URL}/token",
            data={"username": username, "password": password},
            headers={"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        )
        self.assertEqual(response.status_code, 200)
        return response.json()["access_token"]

    def create_point(self, token, description, latitude, longitude, created_at):
        response = requests.post(
            f"{self.BASE_URL}/points/",
            json={
                "description": description,
                "latitude": latitude,
                "longitude": longitude,
                "created_at": created_at
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        self.assertEqual(response.status_code, 200)
        return response.json()

    def delete_point(self, point_id, token):
        response = requests.delete(
            f"{self.BASE_URL}/points/{point_id}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_create_and_delete_update_point(self):
        # Create user 1
        user_1 = self.create_user("user_1", "password_1")
        token_user_1 = self.request_token("user_1", "password_1")

        # Create user 2
        user_2 = self.create_user("user_2", "password_2")
        token_user_2 = self.request_token("user_2", "password_2")

        # User 1 creates a point
        response_user_1 = self.create_point(
            token=token_user_1,
            description="Test point by user 1",
            latitude="60.5",
            longitude="24.9",
            created_at="2021-06-01T10:00:00.000000Z"
        )
        self.assertEqual(response_user_1["description"], "Test point by user 1")

        # User 2 creates a point
        response_user_2 = self.create_point(
            token=token_user_2,
            description="Test point by user 2",
            latitude="60.22",
            longitude="24.92",
            created_at="2021-06-01T10:00:00.000000Z"
        )
        self.assertEqual(response_user_2["description"], "Test point by user 2")

        # User 2 try to update user 1's point (should fail)
        response_update_user_2 = requests.put(
            f"{self.BASE_URL}/points/{response_user_1['id']}",
            json={"description": "Updated point by user 2"},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user_2}"
            }
        )

        self.assertEqual(response_update_user_2.status_code, 403)

        # User 1 updates their own point
        response_update_user_1 = requests.put(
            f"{self.BASE_URL}/points/{response_user_1['id']}",
            json={"description": "Updated point by user 1"},
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token_user_1}"
            }
        )
        self.assertEqual(response_update_user_1.status_code, 200)

        # Ensure point is updated
        response_get_updated_point = requests.get(
            f"{self.BASE_URL}/points/",
            headers={
                "Accept": "application/json",
            }
        )
        self.assertEqual(response_get_updated_point.json()[1]["description"], "Updated point by user 1")

        # User 2 tries to delete user 1's point (should fail)
        response_delete_user_2 = requests.delete(
            f"{self.BASE_URL}/points/{response_user_1['id']}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {token_user_2}"
            }
        )
        self.assertEqual(response_delete_user_2.status_code, 403)

        # User 1 deletes their own point
        self.delete_point(response_user_1["id"], token_user_1)

        # Ensure point is deleted
        response_points = requests.get(
            f"{self.BASE_URL}/points/",
            headers={
                "Accept": "application/json",
            }
        )
        self.assertEqual(response_points.status_code, 200)
        self.assertEqual(len(response_points.json()), 1)
        self.assertEqual(response_points.json()[0]["description"], "Test point by user 2")


if __name__ == "__main__":
    unittest.main()
