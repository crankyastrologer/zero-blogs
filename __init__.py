import os.path
import pathlib

from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor,CKEditorField
from authlib.integrations.flask_client import OAuth
app = Flask(__name__)
oauth = OAuth(app)
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
# enable code snippet plugin
app.config['CKEDITOR_ENABLE_CODESNIPPET'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'add you own'
app.config['SECRET_KEY'] = 'secret'
app.config['GOOGLE_CLIENT_ID']='secret'
app.config['GOOGLE_CLIENT_SECRET']='secret'
google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)
ckeditor = CKEditor(app)

db = SQLAlchemy(app)
