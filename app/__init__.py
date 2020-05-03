from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import Config
from flask_login import LoginManager

app = Flask(__name__)

login = LoginManager(app)

login.login_view="login_page"
login.login_message_category="info"

app.config.from_object(Config)
bcrypt=Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate( app,db )

from app import routes,models