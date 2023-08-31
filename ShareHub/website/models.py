from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy import DateTime


class file(db.Model):
    idfile = db.Column(db.Integer, primary_key=True)
    namefile = db.Column(db.String(150))
    description = db.Column(db.String(150))
    linkfile = db.Column(db.String(150))
    added = db.Column(DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.String(150), db.ForeignKey('user.emailuser'))


class user(db.Model, UserMixin):
    emailuser = db.Column(db.String(150), primary_key=True)
    nameuser = db.Column(db.String(150))
    passworduser = db.Column(db.String(150))
    files = db.relationship('file')