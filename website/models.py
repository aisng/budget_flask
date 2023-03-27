from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(90), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    password = db.Column(db.String(150), nullable=False)
    entries = db.relationship("Entry", back_populates="user")

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps(self.id)

    @staticmethod
    def verify_reset_token(token, max_age=3600):
        s = Serializer(current_app.config["SECRET_KEY"])
        user_id = s.loads(token, max_age=max_age)
        print(user_id)
        return User.query.get(user_id)


class Entry(db.Model):
    __tablename__ = "entry"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user = db.relationship("User", back_populates="entries")
