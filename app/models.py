from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(300), nullable=False)
    pattern = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
from datetime import datetime, timedelta
from app import db

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    attempts = db.Column(db.Integer, default=0)
    mastery_score = db.Column(db.Float, default=0)

    last_attempted = db.Column(db.DateTime, default=datetime.utcnow)
    next_review = db.Column(db.DateTime, default=datetime.utcnow)

    def update_review_schedule(self):
        """
        Spaced repetition logic:
        Higher mastery = longer review interval
        """
        interval_days = max(1, int(self.mastery_score / 20))
        self.next_review = datetime.utcnow() + timedelta(days=interval_days)