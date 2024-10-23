from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.chat_service import ChatService
from services.streaming_assistant import start_conversation, send_message

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

@chat_blueprint.route('/chat/message', methods=['GET'])
def receive_message():
    word = request.args.get('word')
    translation = request.args.get('translation')
    msg = f'The translation of the word "{word}" to Dutch is "{translation}".'
    send_message(msg)
    return Response(status=200)

@chat_blueprint.route('/chat/stream', methods=['GET'])
def stream():
    return Response(start_conversation(), content_type='text/event-stream')
