from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    # One of the following roles: Headmaster, Professor, QA Officer
    role = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))

    # Relationships
    objections = db.relationship("Objection", backref="user", lazy=True)

    # Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def objection_count(self):
        return len(self.objections)

    def __repr__(self):
        out = "\n"
        out += f"Role {self.role} \n"
        out += f"Name {self.name} \n"
        out += f"Email {self.email} \n"
        out += f"Department {self.department.name} \n"
        return out

    def jsonify(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "department": self.department.name,
            "email": self.email,
        }
