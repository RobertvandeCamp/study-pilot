from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.chat_service import ChatService

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

def event_stream():
    while True:
        # Placeholder for actual streaming logic
        yield 'data: {}\n\n'.format('message')

@chat_blueprint.route('/chat/stream', methods=['GET'])
def stream():
    return Response(stream_with_context(event_stream()), content_type='text/event-stream')
