from __init__ import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_history = db.Column(db.PickleType, nullable=False, default=[])
