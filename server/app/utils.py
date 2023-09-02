# Description: This file contains helper functions to add sample data to the database for testing
# and admin purposes.
import logging

from app import app, db
from app.models import Department, Objection, Score, User

# initialize logging
logging.basicConfig(level=logging.INFO)


def commit_to_db(obj):
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f"Database error: {e}")
        raise


def add_department(name):
    department = Department(name=name)
    try:
        commit_to_db(department)
        logging.info(f"Added department: {name}")
        return department
    except:
        logging.error(f"Couldn't add department: {name}")
        return None


def add_user(name, email, password, role, department_name):
    department = Department.query.filter_by(name=department_name).first()

    if not department:
        logging.error(f"Department '{department_name}' not found!")
        return None

    user = User(name=name, email=email, role=role, department=department)
    user.set_password(password)

    try:
        commit_to_db(user)
        logging.info(f"Added user: {email}")
        return user
    except:
        logging.error(f"Couldn't add user: {email}")
        return None


def add_score(professor_email, score_value):
    # Get the user id of the professor
    professor = User.query.filter_by(email=professor_email).first()

    if not professor:
        logging.error(f"Professor with email {professor_email} not found!")
        return None

    score = Score(user_id=professor.id, score_value=score_value)

    try:
        commit_to_db(score)
        logging.info(f"Added score: {score_value}")
        return score

    except:
        logging.error(f"Couldn't add score: {score_value}")
        return None


def add_sample_data():
    with app.app_context():
        # Add Departments
        dept1 = add_department("Computer Science")
        dept2 = add_department("Electrical Engineering")

        # Add Users for Computer Science Department
        add_user(
            "Alice Headmaster",
            "alice.headmaster@cs.edu",
            "password",
            "Headmaster",
            "Computer Science",
        )
        add_user(
            "Bob Professor",
            "bob.professor@cs.edu",
            "password",
            "Professor",
            "Computer Science",
        )
        add_user(
            "Charlie QA",
            "charlie.qa@cs.edu",
            "password",
            "QA Officer",
            "Computer Science",
        )

        # Add Users for Electrical Engineering Department
        add_user(
            "Dave Headmaster",
            "dave.headmaster@ee.edu",
            "password",
            "Headmaster",
            "Electrical Engineering",
        )
        add_user(
            "Eve Professor",
            "eve.professor@ee.edu",
            "password",
            "Professor",
            "Electrical Engineering",
        )
        add_user(
            "Frank QA",
            "frank.qa@ee.edu",
            "password",
            "QA Officer",
            "Electrical Engineering",
        )

        # Add Scores
        add_score("bob.professor@cs.edu", 82)
        add_score("eve.professor@ee.edu", 90)

        # Get a list of all professors' user ids
        # professor_ids = [
        #     professor.id for professor in User.query.filter_by(role="Professor").all()
        # ]

        # # Add Objections
        # objection1 = Objection(
        #     text="I disagree with this score because...",
        #     score_id=1,
        #     user_id=professor_ids[0],
        # )
        # objection2 = Objection(
        #     text="I disagree with this score because...",
        #     score_id=2,
        #     user_id=professor_ids[1],
        # )

        # db.session.add(objection1)
        # db.session.add(objection2)

        # db.session.commit()
