import os
from werkzeug.datastructures import FileStorage
from config.config import Config


def allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed

    Args:
        filename: Name of the file

    Returns:
        True if extension is allowed, False otherwise
    """
    if '.' not in filename:
        return False

    ext = filename.rsplit('.', 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS


def validate_image_upload(file: FileStorage) -> tuple[bool, str]:
    """
    Validate uploaded image file

    Args:
        file: FileStorage object from Flask

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file:
        return False, "No file provided"

    if file.filename == '':
        return False, "No file selected"

    if not allowed_file(file.filename):
        return False, f"File type not allowed. Allowed types: {', '.join(Config.ALLOWED_EXTENSIONS)}"

    return True, ""


def validate_garment_data(data: dict) -> tuple[bool, str]:
    """
    Validate garment data

    Args:
        data: Dictionary containing garment information

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['name', 'category']

    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"

    return True, ""


def validate_outfit_data(data: dict) -> tuple[bool, str]:
    """
    Validate outfit data

    Args:
        data: Dictionary containing outfit information

    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['name', 'garment_ids']

    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    if not isinstance(data['garment_ids'], list) or len(data['garment_ids']) == 0:
        return False, "garment_ids must be a non-empty list"

    return True, ""


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent security issues

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Keep only alphanumeric, dots, hyphens, and underscores
    import re
    filename = re.sub(r'[^\w\.-]', '_', filename)

    # Remove multiple consecutive dots
    filename = re.sub(r'\.{2,}', '.', filename)

    return filename
