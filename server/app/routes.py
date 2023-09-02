import os
import logging
import pandas as pd
from json import JSONEncoder
from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_mail import Message
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from app import app, db
from app.auth import role_required
from app.models import Objection, Score, User
from app.utils import add_department, add_user


# Initialize logger
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv", "xlsx"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def send_email(subject, recipients, text_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    mail.send(msg)


# Default route for info
@app.route("/")
def index():
    return jsonify({"message": "Welcome to the Score Management System!"}), 200


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()

    if user and user.check_password(data["password"]):
        logger.info(f"User {user.email} logged in successfully.")
        access_token = create_access_token(identity=user.id)
        return (
            jsonify(
                {
                    "message": "Logged in successfully!",
                    "token": access_token,
                    "role": user.role,
                }
            ),
            200,
        )
    else:
        logger.warning(f"Failed login attempt for {data['email']}.")
        return jsonify({"message": "Invalid credentials!"}), 401


@app.route("/upload-scores-csv", methods=["POST"])
@role_required("Headmaster")
def upload_scores_csv():
    if "file" not in request.files:
        logger.warning("No file part")
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]

    if file.filename == "":
        logger.warning("No selected file")
        return jsonify({"message": "No selected file"}), 400

    if not allowed_file(file.filename):
        # Delete the uploaded file if it's not a CSV or XLSX file.
        os.remove(filepath)
        logger.warning("Invalid file type")
        return jsonify({"message": "Invalid file type"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        current_user_id = get_jwt_identity()
        current_user = db.session.get(User, current_user_id)

        # Read the CSV file or XLSX file
        if filename.endswith(".csv"):
            data = pd.read_csv(filepath, encoding="utf-8")
        elif filename.endswith(".xlsx"):
            data = pd.read_excel(
                filepath, engine="openpyxl", sheet_name=0, encoding="utf-8"
            )

        # Assuming the CSV has columns 'email' and 'score'
        for index, row in data.iterrows():
            professor = User.query.filter_by(
                email=row["email"], role="Professor"
            ).first()

            error_message = (
                "Professor with email "
                + row["email"]
                + " either doesn't exist or doesn't belong to your department!"
            )

            # Check if professor exists and belongs to the same department as the headmaster
            if not professor or professor.department_id != current_user.department_id:
                logger.warning(error_message)

                return jsonify({"message": error_message}), 400

            score = Score(user_id=professor.id, score_value=row["score"])
            db.session.add(score)

        db.session.commit()

        # Delete the uploaded file
        os.remove(filepath)

        return jsonify({"message": "Scores uploaded successfully!"}), 200
    else:
        # Delete the uploaded file
        os.remove(filepath)
        logger.warning("Invalid file type")
        return jsonify({"message": "Invalid file type"}), 400


@app.route("/get-scores", methods=["GET"])
@role_required("Professor")
def get_scores():
    current_user_id = get_jwt_identity()
    scores = Score.query.filter_by(user_id=current_user_id).all()

    if not scores:
        return jsonify({"message": "No scores found"}), 200

    scores_list = []
    for score in scores:
        scores_list.append(
            {
                "id": score.id,
                "score_value": score.score_value,
                "status": score.status,
                "objection": score.objection.text
                if score.status == "objected"
                else None,
            }
        )

    return jsonify({"scores": scores_list}), 200


@app.route("/object-score", methods=["POST"])
@role_required("Professor")
def object_score():
    data = request.get_json()
    score_id = data.get("score_id")
    objection_text = data.get("objection_text")

    if not score_id or not objection_text:
        return jsonify({"error": "Score ID or objection text not provided"}), 400

    score = db.session.get(Score, score_id)

    if not score:
        return jsonify({"error": "Score not found"}), 404

    current_user_id = get_jwt_identity()

    # Check if the score belongs to the current user
    if score.user_id != current_user_id:
        return jsonify({"error": "Access denied"}), 403

    current_user = db.session.get(User, current_user_id)

    # Create an objection and associate it with the score and the user
    objection = Objection(text=objection_text, score=score, user=current_user)
    db.session.add(objection)

    score.status = "objected"
    db.session.commit()

    return jsonify({"message": "Objection recorded successfully"}), 200


@app.route("/agree-score", methods=["POST"])
@role_required("Professor")
def agree_score():
    data = request.get_json()
    score_id = data.get("score_id")
    current_user_id = get_jwt_identity()

    if not score_id:
        return jsonify({"error": "Score ID not provided"}), 400

    score = db.session.get(Score, score_id)

    if not score:
        return jsonify({"error": "Score not found"}), 404

    # Check if the score belongs to the current user
    if score.user_id != current_user_id:
        return jsonify({"error": "Access denied"}), 403

    score.status = "agreed"
    db.session.commit()

    return jsonify({"message": "Score agreed successfully"}), 200


# view objections, can be accessed by headmaster or quality assurance
@app.route("/view-objections", methods=["GET"])
@role_required(["Headmaster", "Quality Assurance Officer"])
def view_objections():
    objections = Objection.query.all()
    objections_list = []

    for objection in objections:
        objections_list.append(
            {
                "id": objection.id,
                "text": objection.text,
                "score_id": objection.score_id,
                "user_id": objection.user_id,
            }
        )

    return jsonify({"objections": objections_list}), 200


@app.route("/view-objections/<int:objection_id>", methods=["GET"])
@role_required(["Headmaster", "Quality Assurance Officer"])
def view_objection(objection_id):
    objection = db.session.get(Objection, objection_id)

    if not objection:
        return jsonify({"error": "Objection not found"}), 404

    return jsonify({"objection": objection.text}), 200


# Route to verify the token
@app.route("/verify-token", methods=["GET"])
def verify_token():
    try:

        @jwt_required()
        def verify():
            return jsonify({"message": "Token is valid"}), 200

        return verify()
    except Exception as e:
        logger.error(f"Error verifying token: {e}")
        return jsonify({"message": "Invalid token"}), 401


# Secure endpoint to get user info
@app.route("/user", methods=["GET"])
@jwt_required()
def get_user_info():
    current_user = get_jwt_identity()
    user_info = User.query.filter_by(id=current_user).first()
    if user_info:
        return user_info.jsonify(), 200
    else:
        return jsonify({"msg": "User not found"}), 404


# List of all professors in the same department as the headmaster
@app.route("/professors", methods=["GET"])
@role_required("Headmaster")
def get_professors():
    current_user_id = get_jwt_identity()
    current_user = db.session.get(User, current_user_id)
    professors = User.query.filter_by(
        department_id=current_user.department_id, role="Professor"
    ).all()
    professors_list = []

    for professor in professors:
        professors_list.append(
            {
                "id": professor.id,
                "name": professor.name,
                "email": professor.email,
                "department": professor.department.name,
            }
        )

    return jsonify({"professors": professors_list}), 200
