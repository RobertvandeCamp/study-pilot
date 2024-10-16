import unittest
from services.chat_service import ChatService
from models.user import User
from models.conversation import Conversation
from unittest.mock import patch, MagicMock

class TestChatService(unittest.TestCase):

    @patch('services.chat_service.openai.Completion.create')
    @patch('services.chat_service.db.session')
    @patch('services.chat_service.User.query')
    @patch('services.chat_service.Conversation.query')
    def test_handle_user_input_new_user(self, mock_conversation_query, mock_user_query, mock_db_session, mock_openai_create):
        mock_user_query.get.return_value = None
        mock_conversation_query.filter_by.return_value.first.return_value = None
        mock_openai_create.return_value = {'id': 'test_thread_id', 'choices': [{'text': 'test_response'}]}

        chat_service = ChatService()
        response = chat_service.handle_user_input(1, 'Hello')

        self.assertEqual(response, 'test_response')
        mock_db_session.add.assert_called()
        mock_db_session.commit.assert_called()

    @patch('services.chat_service.openai.Completion.create')
    @patch('services.chat_service.db.session')
    @patch('services.chat_service.User.query')
    @patch('services.chat_service.Conversation.query')
    def test_handle_user_input_existing_user(self, mock_conversation_query, mock_user_query, mock_db_session, mock_openai_create):
        mock_user = MagicMock()
        mock_user.conversation_history = []
        mock_user_query.get.return_value = mock_user
        mock_conversation = MagicMock()
        mock_conversation.thread_id = 'test_thread_id'
        mock_conversation_query.filter_by.return_value.first.return_value = mock_conversation
        mock_openai_create.return_value = {'choices': [{'text': 'test_response'}]}

        chat_service = ChatService()
        response = chat_service.handle_user_input(1, 'Hello')

        self.assertEqual(response, 'test_response')
        mock_db_session.commit.assert_called()

    @patch('services.chat_service.openai.Completion.retrieve')
    @patch('services.chat_service.Conversation.query')
    def test_get_latest_response(self, mock_conversation_query, mock_openai_retrieve):
        mock_conversation = MagicMock()
        mock_conversation.thread_id = 'test_thread_id'
        mock_conversation_query.filter_by.return_value.first.return_value = mock_conversation
        mock_openai_retrieve.return_value = {'choices': [{'text': 'test_response'}]}

        chat_service = ChatService()
        response = chat_service.get_latest_response(1)

        self.assertEqual(response, 'test_response')

if __name__ == '__main__':
    unittest.main()
