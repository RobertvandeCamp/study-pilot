import unittest
from flask import Flask
from flask.testing import FlaskClient
from app import app, db
from models.user import User
from models.conversation import Conversation

class ChatRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_chat_route(self):
        response = self.client.post('/chat', json={'input': 'Hello', 'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)

    def test_latest_response_route(self):
        with self.app.app_context():
            user = User(id=1)
            db.session.add(user)
            db.session.commit()

            conversation = Conversation(user_id=1, thread_id='test_thread_id')
            db.session.add(conversation)
            db.session.commit()

        response = self.client.get('/chat/latest', query_string={'user_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json)

if __name__ == '__main__':
    unittest.main()
