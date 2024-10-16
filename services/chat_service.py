import openai
from app import db
from models.user import User
from models.conversation import Conversation
from dotenv import load_dotenv
import os

class ChatService:
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def handle_user_input(self, user_id, user_input):
        user = User.query.get(user_id)
        if not user:
            user = User(id=user_id)
            db.session.add(user)
            db.session.commit()

        conversation = Conversation.query.filter_by(user_id=user_id).first()
        if not conversation:
            response = openai.Completion.create(
                engine="davinci",
                prompt=user_input,
                max_tokens=150
            )
            conversation = Conversation(user_id=user_id, thread_id=response['id'])
            db.session.add(conversation)
            db.session.commit()
        else:
            response = openai.Completion.create(
                engine="davinci",
                prompt=user_input,
                max_tokens=150,
                conversation_id=conversation.thread_id
            )

        user.conversation_history.append(user_input)
        db.session.commit()

        return response['choices'][0]['text']

    def get_latest_response(self, user_id):
        conversation = Conversation.query.filter_by(user_id=user_id).first()
        if not conversation:
            return None

        response = openai.Completion.retrieve(conversation.thread_id)
        return response['choices'][0]['text']
