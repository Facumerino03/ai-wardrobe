import torch
from sentence_transformers import SentenceTransformer
from PIL import Image
from typing import List, Union
import numpy as np
from config.config import Config


class EmbeddingsService:
    """Service for generating embeddings using CLIP/Sentence Transformers"""

    def __init__(self):
        self.model_name = Config.EMBEDDINGS_MODEL
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the embeddings model"""
        try:
            print(f"Loading embeddings model: {self.model_name} on {self.device}")
            # Load model on CPU first, then move to device if needed
            # This avoids the "Cannot copy out of meta tensor" error
            self.model = SentenceTransformer(self.model_name, device='cpu')

            # Move to target device if not CPU
            if self.device != 'cpu':
                try:
                    self.model = self.model.to(self.device)
                except Exception as device_error:
                    print(f"Warning: Could not move model to {self.device}: {device_error}")
                    print("Continuing with CPU device")
                    self.device = 'cpu'

            print(f"Embeddings model loaded successfully on {self.device}")
        except Exception as e:
            print(f"Error loading embeddings model: {e}")
            raise

    def encode_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """
        Generate embeddings for text

        Args:
            text: Single text string or list of text strings

        Returns:
            numpy array of embeddings
        """
        if isinstance(text, str):
            text = [text]

        try:
            embeddings = self.model.encode(text, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            print(f"Error encoding text: {e}")
            raise

    def encode_image(self, image_path: str) -> np.ndarray:
        """
        Generate embeddings for an image

        Args:
            image_path: Path to the image file

        Returns:
            numpy array of image embedding
        """
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')

            # Generate embedding
            embedding = self.model.encode(image, convert_to_numpy=True)

            return embedding
        except Exception as e:
            print(f"Error encoding image: {e}")
            raise

    def encode_images(self, image_paths: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple images

        Args:
            image_paths: List of image file paths

        Returns:
            numpy array of image embeddings
        """
        try:
            images = [Image.open(path).convert('RGB') for path in image_paths]
            embeddings = self.model.encode(images, convert_to_numpy=True)
            return embeddings
        except Exception as e:
            print(f"Error encoding images: {e}")
            raise

    def encode_multimodal(self, text: str, image_path: str) -> np.ndarray:
        """
        Generate combined embedding for text and image

        Args:
            text: Text description
            image_path: Path to image file

        Returns:
            Combined embedding (average of text and image embeddings)
        """
        try:
            text_embedding = self.encode_text(text)
            image_embedding = self.encode_image(image_path)

            # Si text_embedding es 2D (por ejemplo, shape (1, 512)), aplanarlo
            if text_embedding.ndim > 1:
                text_embedding = text_embedding.flatten()
            
            # Si image_embedding es 2D, aplanarlo también
            if image_embedding.ndim > 1:
                image_embedding = image_embedding.flatten()

            # Average the embeddings
            combined = (text_embedding + image_embedding) / 2

            return combined
        except Exception as e:
            print(f"Error encoding multimodal data: {e}")
            raise

    def compute_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Compute cosine similarity between two embeddings

        Args:
            embedding1: First embedding
            embedding2: Second embedding

        Returns:
            Similarity score (0-1)
        """
        try:
            # Normalize embeddings
            embedding1 = embedding1 / np.linalg.norm(embedding1)
            embedding2 = embedding2 / np.linalg.norm(embedding2)

            # Compute cosine similarity
            similarity = np.dot(embedding1, embedding2)

            return float(similarity)
        except Exception as e:
            print(f"Error computing similarity: {e}")
            raise


# Singleton instance
_embeddings_service = None


def get_embeddings_service() -> EmbeddingsService:
    """Get singleton instance of EmbeddingsService"""
    global _embeddings_service
    if _embeddings_service is None:
        _embeddings_service = EmbeddingsService()
    return _embeddings_service
