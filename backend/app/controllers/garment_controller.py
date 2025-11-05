from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

from app.models import Garment
from app.services import get_chroma_service, get_llm_service
from app.utils import (
    validate_image_upload,
    validate_garment_data,
    sanitize_filename,
    get_image_dominant_color_name,
    resize_image
)
from config.config import Config

garment_bp = Blueprint('garment', __name__, url_prefix='/api/garments')


@garment_bp.route('/', methods=['POST'])
def create_garment():
    """Upload and create a new garment"""
    try:
        # Validate file upload
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        is_valid, error_msg = validate_image_upload(file)

        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Get form data
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '').strip()
        color = request.form.get('color', '').strip()
        style = request.form.get('style', '').strip()
        season = request.form.get('season', '').split(',') if request.form.get('season') else []
        description = request.form.get('description', '').strip()
        tags = request.form.get('tags', '').split(',') if request.form.get('tags') else []
        user_id = request.form.get('user_id', 'default_user')

        # Validate required fields
        garment_data = {
            'name': name,
            'category': category,
            'color': color,
            'style': style,
            'season': season,
            'description': description,
            'tags': tags,
            'user_id': user_id
        }

        is_valid, error_msg = validate_garment_data(garment_data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        # Save image
        filename = secure_filename(file.filename)
        filename = f"{uuid.uuid4()}_{sanitize_filename(filename)}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, filename)

        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        file.save(file_path)

        # Resize image for optimization
        resized_path = os.path.join(Config.UPLOAD_FOLDER, f"resized_{filename}")
        resize_image(file_path, resized_path, max_size=(800, 800))

        # Auto-detect color if not provided
        if not color:
            try:
                color = get_image_dominant_color_name(resized_path)
                garment_data['color'] = color
            except:
                garment_data['color'] = 'unknown'

        # Create garment object
        garment = Garment(
            user_id=user_id,
            name=name,
            category=category,
            color=garment_data['color'],
            style=style,
            season=season,
            image_path=resized_path,
            description=description,
            tags=tags
        )

        # Analyze with LLM (enhance metadata)
        try:
            llm_service = get_llm_service()
            enhanced_data = llm_service.analyze_garment_image(garment.to_dict())

            # Update garment with enhanced data
            garment.description = enhanced_data.get('description', garment.description)
            garment.style = enhanced_data.get('style', garment.style)
            garment.season = enhanced_data.get('season', garment.season)
            garment.tags = enhanced_data.get('tags', garment.tags)
            garment.metadata = enhanced_data.get('metadata', {})
        except Exception as e:
            print(f"LLM analysis failed: {e}")
            # Continue without LLM enhancement

        # Store in ChromaDB
        chroma_service = get_chroma_service()
        chroma_service.add_garment(
            garment_id=garment.id,
            garment_data=garment.to_dict(),
            image_path=resized_path
        )

        return jsonify({
            'success': True,
            'garment': garment.to_dict()
        }), 201

    except Exception as e:
        print(f"Error creating garment: {e}")
        return jsonify({'error': str(e)}), 500


@garment_bp.route('/', methods=['GET'])
def get_all_garments():
    """Get all garments, optionally filtered by user"""
    try:
        user_id = request.args.get('user_id')

        chroma_service = get_chroma_service()
        garments = chroma_service.get_all_garments(user_id=user_id)

        return jsonify({
            'success': True,
            'count': len(garments),
            'garments': garments
        }), 200

    except Exception as e:
        print(f"Error getting garments: {e}")
        return jsonify({'error': str(e)}), 500


@garment_bp.route('/<garment_id>', methods=['GET'])
def get_garment(garment_id):
    """Get a specific garment by ID"""
    try:
        chroma_service = get_chroma_service()
        garment = chroma_service.get_garment(garment_id)

        if not garment:
            return jsonify({'error': 'Garment not found'}), 404

        return jsonify({
            'success': True,
            'garment': garment
        }), 200

    except Exception as e:
        print(f"Error getting garment: {e}")
        return jsonify({'error': str(e)}), 500


@garment_bp.route('/search', methods=['POST'])
def search_garments():
    """Search garments using text or image query"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        query = data.get('query', '').strip()
        user_id = data.get('user_id')
        filters = data.get('filters', {})
        n_results = data.get('n_results', 10)

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        chroma_service = get_chroma_service()
        results = chroma_service.search_similar_garments(
            query=query,
            n_results=n_results,
            user_id=user_id,
            filters=filters
        )

        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        }), 200

    except Exception as e:
        print(f"Error searching garments: {e}")
        return jsonify({'error': str(e)}), 500


@garment_bp.route('/<garment_id>', methods=['PUT'])
def update_garment(garment_id):
    """Update a garment"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Get existing garment
        chroma_service = get_chroma_service()
        garment_data = chroma_service.get_garment(garment_id)

        if not garment_data:
            return jsonify({'error': 'Garment not found'}), 404

        # Update fields
        garment = Garment.from_dict(garment_data)

        if 'name' in data:
            garment.name = data['name']
        if 'category' in data:
            garment.category = data['category']
        if 'color' in data:
            garment.color = data['color']
        if 'style' in data:
            garment.style = data['style']
        if 'season' in data:
            garment.season = data['season']
        if 'description' in data:
            garment.description = data['description']
        if 'tags' in data:
            garment.tags = data['tags']

        garment.update_timestamp()

        # Update in ChromaDB
        chroma_service.update_garment(
            garment_id=garment_id,
            garment_data=garment.to_dict(),
            image_path=garment.image_path
        )

        return jsonify({
            'success': True,
            'garment': garment.to_dict()
        }), 200

    except Exception as e:
        print(f"Error updating garment: {e}")
        return jsonify({'error': str(e)}), 500


@garment_bp.route('/<garment_id>', methods=['DELETE'])
def delete_garment(garment_id):
    """Delete a garment"""
    try:
        chroma_service = get_chroma_service()

        # Get garment to delete image file
        garment = chroma_service.get_garment(garment_id)

        if not garment:
            return jsonify({'error': 'Garment not found'}), 404

        # Delete from ChromaDB
        chroma_service.delete_garment(garment_id)

        # Delete image file
        try:
            if garment.get('image_path') and os.path.exists(garment['image_path']):
                os.remove(garment['image_path'])
        except Exception as e:
            print(f"Error deleting image file: {e}")

        return jsonify({
            'success': True,
            'message': 'Garment deleted successfully'
        }), 200

    except Exception as e:
        print(f"Error deleting garment: {e}")
        return jsonify({'error': str(e)}), 500


@garment_bp.route('/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    """Serve uploaded images"""
    try:
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    except Exception as e:
        return jsonify({'error': 'Image not found'}), 404
