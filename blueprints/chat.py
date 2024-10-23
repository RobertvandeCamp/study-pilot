from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.chat_service import ChatService
from services.streaming_assistant import start_conversation

chat_blueprint = Blueprint('chat', __name__)

@chat_blueprint.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('input')
    user_id = request.json.get('user_id')
    if not user_input or not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    chat_service = ChatService()
    response = chat_service.handle_user_input(user_id, user_input)
    return jsonify({'response': response})

@chat_blueprint.route('/chat/latest', methods=['GET'])
def latest_response():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'Invalid input'}), 400

    chat_service = ChatService()
    response = chat_service.get_latest_response(user_id)
    return jsonify({'response': response})

@chat_blueprint.route('/chat/stream', methods=['GET'])
def stream():
    assistant = snape  # or any other assistant you want to use
    thread = client.beta.threads.create()
    send_message(thread.id, "The translation of the word 'Building' to Dutch is 'Gebouw'.")
    return Response(start_conversation(assistant, thread), content_type='text/event-stream')
