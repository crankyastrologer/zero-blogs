from datetime import datetime


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, Email, DataRequired

from __init__ import db,CKEditorField

class MessageDatabase(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False)
    email_address = db.Column(db.String(length=50), nullable=False)
    message = db.Column(db.String(length=500), nullable=False)


class MessageForm(FlaskForm):
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    message = StringField(label='Message:', validators=[Length(min=5, max=500), DataRequired()])
    submit = SubmitField(label="Send message")


class Post(FlaskForm):
    title = StringField('Title')
    body = CKEditorField('Body')  # <--
    submit = SubmitField('Submit')


class postdbs(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    body = db.Column(db.String(length=5000), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime, default=datetime.now)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=50), nullable=False)
    posts = db.relationship('postdbs', backref='owned_user', lazy=True)
