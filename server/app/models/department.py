from app import db


class Department(db.Model):
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    users = db.relationship("User", backref="department", lazy=True)

    # Methods
    def jsonify(self):
        return {"id": self.id, "name": self.name}
