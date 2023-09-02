from app import db


class Objection(db.Model):
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    score_id = db.Column(db.Integer, db.ForeignKey("score.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # The score id and user id are not unique together, but the combination of the two should be unique.
    __table_args__ = (
        db.UniqueConstraint("score_id", "user_id", name="unique_score_user"),
    )

    # Methods
    def jsonify(self):
        return {
            "id": self.id,
            "text": self.text,
            "score_id": self.score_id,
            "user_id": self.user_id,
        }
