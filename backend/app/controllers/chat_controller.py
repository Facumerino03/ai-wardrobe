from flask import Blueprint, request, jsonify
from typing import List, Dict

from app.services import get_llm_service

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

# In-memory conversation storage (for simplicity)
# In production, use a proper database or session management
conversations: Dict[str, List[Dict]] = {}


@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Send a message to the fashion assistant"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default_user')
        session_id = data.get('session_id', 'default_session')

        if not message:
            return jsonify({'error': 'Message is required'}), 400

        # Get or create conversation history
        conversation_key = f"{user_id}:{session_id}"

        if conversation_key not in conversations:
            conversations[conversation_key] = []

        conversation_history = conversations[conversation_key]

        # Get user context (optional)
        user_context = data.get('context', {})

        # Get LLM response
        llm_service = get_llm_service()
        response = llm_service.chat_about_fashion(
            user_message=message,
            conversation_history=conversation_history,
            user_context=user_context
        )

        # Update conversation history
        conversation_history.append({
            "role": "user",
            "content": message
        })
        conversation_history.append({
            "role": "assistant",
            "content": response
        })

        # Limit conversation history to last 20 messages
        if len(conversation_history) > 20:
            conversations[conversation_key] = conversation_history[-20:]

        return jsonify({
            'success': True,
            'message': response,
            'session_id': session_id
        }), 200

    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_conversation_history(session_id):
    """Get conversation history for a session"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        conversation_key = f"{user_id}:{session_id}"

        history = conversations.get(conversation_key, [])

        return jsonify({
            'success': True,
            'history': history
        }), 200

    except Exception as e:
        print(f"Error getting conversation history: {e}")
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/clear/<session_id>', methods=['DELETE'])
def clear_conversation(session_id):
    """Clear conversation history"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        conversation_key = f"{user_id}:{session_id}"

        if conversation_key in conversations:
            del conversations[conversation_key]

        return jsonify({
            'success': True,
            'message': 'Conversation cleared'
        }), 200

    except Exception as e:
        print(f"Error clearing conversation: {e}")
        return jsonify({'error': str(e)}), 500
