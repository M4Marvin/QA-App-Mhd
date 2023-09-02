import unittest
from app import app, db
from app.utils import add_sample_data
from app.models import Score, Objection, User
import pprint


class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object("config_test")
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            add_sample_data()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_upload_scores(self):
        # Log in as Headmaster
        token = self.login("alice.headmaster@cs.edu", "password").json["token"]

        data = {"file": (open("data.csv", "rb"), "sample_scores.csv")}
        response = self.client.post(
            "/upload-scores-csv",
            data=data,
            content_type="multipart/form-data",
            headers={"Authorization": f"Bearer {token}"},
        )
        # pprint.pprint(response.json)
        self.assertEqual(response.status_code, 200)

    def login(self, email, password):
        """Helper method to log in as a user."""
        return self.client.post("/login", json={"email": email, "password": password})

    def test_view_scores(self):
        # Log in as Professor
        token = self.login("bob.professor@cs.edu", "password").json["token"]

        response = self.client.get(
            "/view-scores", headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)

    def test_agree_score(self):
        # Log in as Professor
        token = self.login("bob.professor@cs.edu", "password").json["token"]

        # Assuming you have a sample score with ID 1 for this professor in your sample data
        response = self.client.post(
            "/agree-score",
            json={"score_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )
        # print(response.json)

        self.assertEqual(response.status_code, 200)

        # Check the status of the score in the database
        with app.app_context():
            score = db.session.get(Score, 1)
            self.assertEqual(score.status, "agreed")

    def test_object_score(self):
        # Log in as Professor
        token = self.login("bob.professor@cs.edu", "password").json["token"]

        objection_text = "I disagree with this score because..."
        response = self.client.post(
            "/object-score",
            json={"score_id": 1, "objection_text": objection_text, "user_id": 1},
            headers={"Authorization": f"Bearer {token}"},
        )

        self.assertEqual(response.status_code, 200)

        # Check the status of the score and the objection in the database
        with app.app_context():
            score = db.session.get(Score, 1)
            self.assertEqual(score.status, "objected")

            objection = Objection.query.filter_by(score_id=1).first()
            self.assertIsNotNone(objection)
            self.assertEqual(objection.text, objection_text)

    def test_view_objections(self):
        # Login first as Headmaster and object to a score
        token = self.login("alice.headmaster@cs.edu", "password").json["token"]

        response = self.client.get(
            "/view-objections", headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(response.status_code, 200)
        # print(response.json)

    # ... Add more tests as necessary for other routes


if __name__ == "__main__":
    unittest.main()
