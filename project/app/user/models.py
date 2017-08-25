from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    paste_count = db.Column(db.Integer)
    user_type = db.Column(db.Integer)

    def __init__(self, username, email, password, paste_count, user_type):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.paste_count = paste_count
        self.user_type = user_type

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'paste_count': self.paste_count,
            'user_type': self.user_type,
        }

    def __repr__(self):
        return "User<%d> %s" % (self.id, self.username)
