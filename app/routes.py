# from flask import Blueprint, jsonify

# main = Blueprint("main", __name__)

# @main.route("/")
# def home():
#     return jsonify({"message": "Grindsa SaaS Backend Running"})
from datetime import datetime
from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Question, UserProgress

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return jsonify({"message": "Grindsa SaaS Backend Running"})


@main.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@main.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token
    }), 200

@main.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    return jsonify({
        "message": "Access granted",
        "user_id": user_id
    })

@main.route("/questions", methods=["POST"])
@jwt_required()
def create_question():
    user_id = get_jwt_identity()

    data = request.get_json()

    title = data.get("title")
    link = data.get("link")
    pattern = data.get("pattern")
    difficulty = data.get("difficulty")

    if not all([title, link, pattern, difficulty]):
        return jsonify({"error": "All fields required"}), 400

    question = Question(
        title=title,
        link=link,
        pattern=pattern,
        difficulty=difficulty
    )

    db.session.add(question)
    db.session.commit()

    return jsonify({"message": "Question created"}), 201

@main.route("/questions", methods=["GET"])
@jwt_required()
def list_questions():
    questions = Question.query.all()

    output = []

    for q in questions:
        output.append({
            "id": q.id,
            "title": q.title,
            "link": q.link,
            "pattern": q.pattern,
            "difficulty": q.difficulty
        })

    return jsonify(output), 200
@main.route("/questions/<int:question_id>/attempt", methods=["POST"])
@jwt_required()
# def attempt_question(question_id):
#     user_id = int(get_jwt_identity())

#     data = request.get_json()
#     solved = data.get("solved", False)

#     question = Question.query.get(question_id)

#     if not question:
#         return jsonify({"error": "Question not found"}), 404

#     progress = UserProgress.query.filter_by(
#         user_id=user_id,
#         question_id=question_id
#     ).first()

#     if not progress:
#         progress = UserProgress(
#             user_id=user_id,
#             question_id=question_id,
#             attempts=1,
#             solved=solved,
#             mastery_score=1 if solved else 0
#         )
#         db.session.add(progress)
  
#     # db.session.commit()

#     return jsonify({
#         "message": "Attempt recorded",
#         "attempts": progress.attempts,
#         "mastery_score": progress.mastery_score,
#         "solved": progress.solved
#     }), 200

# from flask import request, jsonify
# from flask_jwt_extended import get_jwt_identity
# from app import db
# from models import Question, UserProgress

def attempt_question(question_id):
    user_id = int(get_jwt_identity())

    data = request.get_json()
    solved = data.get("solved", False)

    question = Question.query.get(question_id)

    if not question:
        return jsonify({"error": "Question not found"}), 404

    progress = UserProgress.query.filter_by(
        user_id=user_id,
        question_id=question_id
    ).first()

    # 🔹 FIRST TIME ATTEMPT
    if not progress:
        progress = UserProgress(
            user_id=user_id,
            question_id=question_id,
            attempts=1,
            mastery_score=15 if solved else 0,
            last_attempted=datetime.utcnow()
        )

        progress.update_review_schedule()
        db.session.add(progress)

    # 🔹 EXISTING PROGRESS UPDATE
    else:
        progress.attempts += 1
        progress.last_attempted = datetime.utcnow()

        if solved:
            progress.mastery_score = min(100, progress.mastery_score + 15)
        else:
            progress.mastery_score = max(0, progress.mastery_score - 5)

        progress.update_review_schedule()

    db.session.commit()

    return jsonify({
        "message": "Attempt recorded",
        "mastery_score": progress.mastery_score,
        "next_review": progress.next_review
    })

@main.route("/progress", methods=["GET"])
@jwt_required()
def view_progress():
    user_id = int(get_jwt_identity())

    progress_records = UserProgress.query.filter_by(user_id=user_id).all()

    output = []

    for p in progress_records:
        question = Question.query.get(p.question_id)

        output.append({
            "question_id": p.question_id,
            "title": question.title,
            "attempts": p.attempts,
            "solved": p.solved,
            "mastery_score": p.mastery_score
        })

    return jsonify(output), 200


@main.route("/review-today", methods=["GET"])
@jwt_required()
def review_today():
    user_id = int(get_jwt_identity())

    due_questions = UserProgress.query.filter(
        UserProgress.user_id == user_id,
        UserProgress.next_review <= datetime.utcnow()
    ).all()

    result = []

    for progress in due_questions:
        question = Question.query.get(progress.question_id)

        result.append({
            "question_id": question.id,
            "title": question.title,
            "difficulty": question.difficulty,
            "mastery_score": progress.mastery_score,
            "next_review": progress.next_review
        })

    return jsonify(result)