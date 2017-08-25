from flask_sqlalchemy import SQLAlchemy
from app import db
import uuid
from datetime import datetime
from dateutil import parser


class Paste(db.Model):
    __tablename__ = 'pastes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    text = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lang = db.Column(db.String(255))
    add_time = db.Column(db.String(255))
    expire_time = db.Column(db.String(255))
    url = db.Column(db.String(500))
    report_count = db.Column(db.Integer)
    paste_type = db.Column(db.String(5))

    def __init__(self, title, text, lang, add_time, expire_time, user_id, url, report_count ,paste_type):
        self.title = title
        self.text = text
        self.lang = lang
        self.add_time = add_time
        self.expire_time = expire_time
        self.user_id = user_id
        self.url = url
        self.report_count = report_count

        self.paste_type = paste_type

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'lang': self.lang,
            'add_time': self.add_time,
            'expire_time': self.expire_time,
            'url': self.url,
            'report_count': self.report_count,
            'paste_type': self.paste_type
        }

    def is_active(self):
        if(parser.parse(self.expire_time) > datetime.now()):
            return True
        else:
            return False

    def __repr__(self):
        return "Paste<%d> %s %s %s %s %s %d" % (self.id, self.title, self.text, self.lang, self.add_time, self.expire_time, self.report_count)
