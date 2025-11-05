import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""

    # Base directory
    BASE_DIR = Path(__file__).parent.parent

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'

    # OpenRouter API
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.1-70b-instruct')
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

    # ChromaDB
    CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY', str(BASE_DIR / 'data' / 'chroma_db'))
    CHROMA_COLLECTION_NAME = 'wardrobe_items'

    # Colab API (Virtual Try-On)
    COLAB_API_URL = os.getenv('COLAB_API_URL')

    # File Upload
    UPLOAD_FOLDER = BASE_DIR / 'app' / 'static' / 'uploads'
    GENERATED_FOLDER = BASE_DIR / 'app' / 'static' / 'generated'
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,webp').split(','))

    # Embeddings
    EMBEDDINGS_MODEL = os.getenv('EMBEDDINGS_MODEL', 'sentence-transformers/clip-ViT-B-32')

    @staticmethod
    def init_app(app):
        """Initialize application"""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)
        os.makedirs(Config.CHROMA_PERSIST_DIRECTORY, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
