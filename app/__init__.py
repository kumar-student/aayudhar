import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
if not os.path.exists(app.config['AVATAR_UPLOAD_FOLDER']):
    os.makedirs(app.config['AVATAR_UPLOAD_FOLDER'])
if not os.path.exists(app.config['IMAGE_UPLOAD_FOLDER']):
    os.makedirs(app.config['IMAGE_UPLOAD_FOLDER'])
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models