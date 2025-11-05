from flask import Blueprint, request, jsonify
import json
from typing import List, Dict

from app.models import Outfit
from app.services import get_chroma_service, get_llm_service
from app.utils import validate_outfit_data

outfit_bp = Blueprint('outfit', __name__, url_prefix='/api/outfits')

# In-memory storage for outfits (for simplicity)
# In production, use a proper database
outfits_db: Dict[str, Outfit] = {}


@outfit_bp.route('/', methods=['POST'])
def create_outfit():
    """Create a new outfit"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate outfit data
        is_valid, error_msg = validate_outfit_data(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Verify that all garments exist
        chroma_service = get_chroma_service()
        garment_ids = data['garment_ids']

        for garment_id in garment_ids:
            garment = chroma_service.get_garment(garment_id)
            if not garment:
                return jsonify({'error': f'Garment {garment_id} not found'}), 404

        # Create outfit
        outfit = Outfit(
            user_id=data.get('user_id', 'default_user'),
            name=data['name'],
            garment_ids=garment_ids,
            occasion=data.get('occasion', ''),
            season=data.get('season', ''),
            style=data.get('style', ''),
            description=data.get('description', ''),
            rating=data.get('rating'),
            tags=data.get('tags', [])
        )

        # Store outfit
        outfits_db[outfit.id] = outfit

        return jsonify({
            'success': True,
            'outfit': outfit.to_dict()
        }), 201

    except Exception as e:
        print(f"Error creating outfit: {e}")
        return jsonify({'error': str(e)}), 500


@outfit_bp.route('/', methods=['GET'])
def get_all_outfits():
    """Get all outfits, optionally filtered by user"""
    try:
        user_id = request.args.get('user_id')

        if user_id:
            filtered_outfits = [
                outfit.to_dict()
                for outfit in outfits_db.values()
                if outfit.user_id == user_id
            ]
        else:
            filtered_outfits = [outfit.to_dict() for outfit in outfits_db.values()]

        return jsonify({
            'success': True,
            'count': len(filtered_outfits),
            'outfits': filtered_outfits
        }), 200

    except Exception as e:
        print(f"Error getting outfits: {e}")
        return jsonify({'error': str(e)}), 500


@outfit_bp.route('/<outfit_id>', methods=['GET'])
def get_outfit(outfit_id):
    """Get a specific outfit by ID"""
    try:
        outfit = outfits_db.get(outfit_id)

        if not outfit:
            return jsonify({'error': 'Outfit not found'}), 404

        # Get garment details
        chroma_service = get_chroma_service()
        garments = []

        for garment_id in outfit.garment_ids:
            garment = chroma_service.get_garment(garment_id)
            if garment:
                garments.append(garment)

        outfit_data = outfit.to_dict()
        outfit_data['garments'] = garments

        return jsonify({
            'success': True,
            'outfit': outfit_data
        }), 200

    except Exception as e:
        print(f"Error getting outfit: {e}")
        return jsonify({'error': str(e)}), 500


@outfit_bp.route('/suggest', methods=['POST'])
def suggest_outfits():
    """Suggest outfit combinations based on user query"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        query = data.get('query', '').strip()
        user_id = data.get('user_id', 'default_user')
        context = data.get('context', {})

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        # Get user's wardrobe
        chroma_service = get_chroma_service()
        all_garments = chroma_service.get_all_garments(user_id=user_id)

        if not all_garments:
            return jsonify({
                'error': 'No garments found in wardrobe. Please add some items first.'
            }), 404

        # Use LLM to suggest outfits
        llm_service = get_llm_service()
        suggestions = llm_service.suggest_outfits(
            user_query=query,
            available_garments=all_garments,
            context=context
        )

        return jsonify(suggestions), 200

    except Exception as e:
        print(f"Error suggesting outfits: {e}")
        return jsonify({'error': str(e)}), 500


@outfit_bp.route('/<outfit_id>', methods=['PUT'])
def update_outfit(outfit_id):
    """Update an outfit"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        outfit = outfits_db.get(outfit_id)

        if not outfit:
            return jsonify({'error': 'Outfit not found'}), 404

        # Update fields
        if 'name' in data:
            outfit.name = data['name']
        if 'garment_ids' in data:
            outfit.garment_ids = data['garment_ids']
        if 'occasion' in data:
            outfit.occasion = data['occasion']
        if 'season' in data:
            outfit.season = data['season']
        if 'style' in data:
            outfit.style = data['style']
        if 'description' in data:
            outfit.description = data['description']
        if 'rating' in data:
            outfit.rating = data['rating']
        if 'tags' in data:
            outfit.tags = data['tags']
        if 'generated_image_path' in data:
            outfit.generated_image_path = data['generated_image_path']

        outfit.update_timestamp()

        return jsonify({
            'success': True,
            'outfit': outfit.to_dict()
        }), 200

    except Exception as e:
        print(f"Error updating outfit: {e}")
        return jsonify({'error': str(e)}), 500


@outfit_bp.route('/<outfit_id>', methods=['DELETE'])
def delete_outfit(outfit_id):
    """Delete an outfit"""
    try:
        if outfit_id not in outfits_db:
            return jsonify({'error': 'Outfit not found'}), 404

        del outfits_db[outfit_id]

        return jsonify({
            'success': True,
            'message': 'Outfit deleted successfully'
        }), 200

    except Exception as e:
        print(f"Error deleting outfit: {e}")
        return jsonify({'error': str(e)}), 500


@outfit_bp.route('/<outfit_id>/rate', methods=['POST'])
def rate_outfit(outfit_id):
    """Rate an outfit (1-5 stars)"""
    try:
        data = request.get_json()

        if not data or 'rating' not in data:
            return jsonify({'error': 'Rating is required'}), 400

        rating = data['rating']

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400

        outfit = outfits_db.get(outfit_id)

        if not outfit:
            return jsonify({'error': 'Outfit not found'}), 404

        outfit.rating = rating
        outfit.update_timestamp()

        return jsonify({
            'success': True,
            'outfit': outfit.to_dict()
        }), 200

    except Exception as e:
        print(f"Error rating outfit: {e}")
        return jsonify({'error': str(e)}), 500
