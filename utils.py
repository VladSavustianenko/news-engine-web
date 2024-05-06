import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:admin' \
#                                                        f'@localhost/portal'
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'

# app.config['SQLALCHEMY_BINDS'] = {
#     'news': f'postgresql://postgres:admin@localhost/news'
# }
app.config['SQLALCHEMY_BINDS'] = {
    'news': f'postgresql://{os.getenv("NEWS_DATABASE_USER")}:{os.getenv("NEWS_DATABASE_PASSWORD")}@{os.getenv("NEWS_DATABASE_HOST")}:{os.getenv("NEWS_DATABASE_PORT")}/{os.getenv("NEWS_DATABASE_NAME")}'
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

db = SQLAlchemy(app)
jwt = JWTManager()
jwt.init_app(app)
