from app import db


class Score(db.Model):
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    score_value = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default="unchecked")

    # Relationships
    objection = db.relationship("Objection", backref="score", uselist=False, lazy=True)

    # Methods
    def jsonify(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "score_value": self.score_value,
            "status": self.status,
        }
