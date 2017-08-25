from flask_sqlalchemy import SQLAlchemy
from app import db


class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    paste_id = db.Column(db.String(100), db.ForeignKey('pastes.url'))
    reason = db.Column(db.String(150))
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, paste_id, reason, reporter_id):
        self.paste_id = paste_id
        self.reason = reason
        self.reporter_id = reporter_id

    def to_dict(self):
        return {
            'id': self.id,
            'paste_id': self.paste_id,
            'reason': self.reason,
            'reporter_id': self.reporter_id,
        }

    def __repr__(self):
        return "reporter_id %d" % self.reporter_id
