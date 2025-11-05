from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid

from app.services import get_tryon_service, get_chroma_service
from app.utils import validate_image_upload, sanitize_filename
from config.config import Config

tryon_bp = Blueprint('tryon', __name__, url_prefix='/api/tryon')


@tryon_bp.route('/generate', methods=['POST'])
def generate_tryon():
    """Generate virtual try-on image"""
    try:
        # Check if person image is uploaded or provided
        person_image_path = None

        if 'person_image' in request.files:
            # User uploaded a person image
            person_file = request.files['person_image']
            is_valid, error_msg = validate_image_upload(person_file)

            if not is_valid:
                return jsonify({'error': f'Person image: {error_msg}'}), 400

            # Save person image
            filename = secure_filename(person_file.filename)
            filename = f"person_{uuid.uuid4()}_{sanitize_filename(filename)}"
            person_image_path = os.path.join(Config.UPLOAD_FOLDER, filename)

            os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
            person_file.save(person_image_path)

        elif request.form.get('person_image_path'):
            # User provided existing person image path
            person_image_path = request.form.get('person_image_path')

            if not os.path.exists(person_image_path):
                return jsonify({'error': 'Person image path does not exist'}), 400

        else:
            return jsonify({'error': 'Person image is required'}), 400

        # Get garment
        garment_id = request.form.get('garment_id')

        if not garment_id:
            return jsonify({'error': 'Garment ID is required'}), 400

        # Retrieve garment from database
        chroma_service = get_chroma_service()
        garment = chroma_service.get_garment(garment_id)

        if not garment:
            return jsonify({'error': 'Garment not found'}), 404

        garment_image_path = garment.get('image_path')

        if not garment_image_path or not os.path.exists(garment_image_path):
            return jsonify({'error': 'Garment image not found'}), 404

        # Generate output path
        output_filename = f"tryon_{uuid.uuid4()}.png"
        output_path = os.path.join(Config.GENERATED_FOLDER, output_filename)

        os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)

        # Call virtual try-on service
        tryon_service = get_tryon_service()
        result = tryon_service.generate_tryon(
            person_image_path=person_image_path,
            garment_image_path=garment_image_path,
            output_path=output_path
        )

        if not result.get('success'):
            return jsonify({
                'success': False,
                'error': result.get('error', 'Virtual try-on failed')
            }), 500

        return jsonify({
            'success': True,
            'message': 'Virtual try-on generated successfully',
            'image_url': f'/api/tryon/images/{output_filename}',
            'image_path': output_path
        }), 200

    except Exception as e:
        print(f"Error generating virtual try-on: {e}")
        return jsonify({'error': str(e)}), 500


@tryon_bp.route('/health', methods=['GET'])
def check_health():
    """Check if virtual try-on API is available"""
    try:
        tryon_service = get_tryon_service()
        is_available = tryon_service.check_api_health()

        return jsonify({
            'success': True,
            'available': is_available,
            'api_url': Config.COLAB_API_URL
        }), 200

    except Exception as e:
        print(f"Error checking try-on health: {e}")
        return jsonify({'error': str(e)}), 500


@tryon_bp.route('/images/<path:filename>', methods=['GET'])
def serve_generated_image(filename):
    """Serve generated try-on images"""
    try:
        return send_from_directory(Config.GENERATED_FOLDER, filename)
    except Exception as e:
        return jsonify({'error': 'Image not found'}), 404
