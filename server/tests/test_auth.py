import unittest
from app import app, db
from app.utils import add_sample_data
from json import JSONEncoder


class DepartmentUserTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object("config_test")
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
            add_sample_data()  # Assuming this sets up both departments and users.

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_db_contents(self):
        with app.app_context():
            from app.models import Department, User, Score, Objection

            print("Departments:")
            for dept in Department.query.all():
                print(f" - {dept.id}. {dept.name}")

            print("Users:")
            for user in User.query.all():
                print(f" - {user.id}. {user.name} ({user.email})")

            print("Scores:")
            for score in Score.query.all():
                print(f" - {score.id}. {score.score_value}")

            print("Objections:")
            for objection in Objection.query.all():
                print(f" - {objection.id}. {objection.text}")

    def test_departments_created(self):
        with app.app_context():
            from app.models import Department

            dept1 = Department.query.filter_by(name="Computer Science").first()
            dept2 = Department.query.filter_by(name="Electrical Engineering").first()
            self.assertIsNotNone(dept1)
            self.assertIsNotNone(dept2)

    def test_users_created(self):
        with app.app_context():
            from app.models import User

            user = User.query.filter_by(email="alice.headmaster@cs.edu").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.name, "Alice Headmaster")

    def test_successful_login(self):
        response = self.client.post(
            "/login", json={"email": "alice.headmaster@cs.edu", "password": "password"}
        )
        self.assertEqual(response.status_code, 200)

    # ... you can add more tests as needed


if __name__ == "__main__":
    unittest.main()
