from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blueprints.chat import chat_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
db = SQLAlchemy(app)

app.register_blueprint(chat_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
