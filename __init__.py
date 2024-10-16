from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chat.db')
db = SQLAlchemy(app)

from models.user import User
from models.conversation import Conversation

with app.app_context():
    db.create_all()

from blueprints.chat import chat_blueprint
app.register_blueprint(chat_blueprint)
