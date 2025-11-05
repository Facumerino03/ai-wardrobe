import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
import json
from config.config import Config
from app.services.embeddings_service import get_embeddings_service


class ChromaService:
    """Service for managing ChromaDB operations"""

    def __init__(self, persist_directory='./data/chroma_db'):
        # Solo inicializar variables, no crear el cliente aquí
        self.persist_directory = Config.CHROMA_PERSIST_DIRECTORY
        self.collection_name = Config.CHROMA_COLLECTION_NAME
        self.client = None
        self.collection = None
        self.embeddings_service = get_embeddings_service()
        self._initialize_client()

    def _initialize_client(self):
        """Initialize ChromaDB client and collection"""
        try:
            print(f"Initializing ChromaDB at: {self.persist_directory}")

            # Create ChromaDB client with persistence - SOLO UNA VEZ
            self.client = chromadb.PersistentClient(
                path=self.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )

            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Wardrobe garment embeddings"}
            )

            print(f"ChromaDB initialized. Collection: {self.collection_name}")
            print(f"Current items in collection: {self.collection.count()}")

        except Exception as e:
            print(f"Error initializing ChromaDB: {e}")
            raise

    def add_garment(self, garment_id: str, garment_data: Dict, image_path: str):
        """
        Add a garment to ChromaDB with its embedding

        Args:
            garment_id: Unique garment identifier
            garment_data: Dictionary containing garment metadata
            image_path: Path to garment image
        """
        try:
            # Asegurarse de que image_path esté en garment_data
            garment_data['image_path'] = image_path
            
            # Generate text description for embedding
            text_description = self._create_text_description(garment_data)

            # Generate multimodal embedding (text + image)
            embedding = self.embeddings_service.encode_multimodal(
                text=text_description,
                image_path=image_path
            )

            # Prepare metadata (ChromaDB requires string values)
            metadata = {
                'name': garment_data.get('name', ''),
                'category': garment_data.get('category', ''),
                'color': garment_data.get('color', ''),
                'style': garment_data.get('style', ''),
                'season': ','.join(garment_data.get('season', [])),
                'tags': ','.join(garment_data.get('tags', [])),
                'user_id': garment_data.get('user_id', ''),
                'image_path': image_path,
                'data': json.dumps(garment_data)  # Store full data as JSON
            }

            # Add to collection
            self.collection.add(
                ids=[garment_id],
                embeddings=[embedding.tolist()],
                metadatas=[metadata],
                documents=[text_description]
            )

            print(f"Added garment {garment_id} to ChromaDB")

        except Exception as e:
            print(f"Error adding garment to ChromaDB: {e}")
            raise

    def search_similar_garments(
        self,
        query: str,
        n_results: int = 5,
        user_id: Optional[str] = None,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar garments using text query

        Args:
            query: Text search query
            n_results: Number of results to return
            user_id: Filter by user ID
            filters: Additional filters (category, color, etc.)

        Returns:
            List of matching garments with metadata
        """
        try:
            # Generate query embedding
            query_embedding = self.embeddings_service.encode_text(query)

            # Build where clause for filtering
            where_clause = {}
            if user_id:
                where_clause['user_id'] = user_id

            if filters:
                for key, value in filters.items():
                    if value:
                        where_clause[key] = value

            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results,
                where=where_clause if where_clause else None
            )

            # Parse and return results
            return self._parse_results(results)

        except Exception as e:
            print(f"Error searching garments: {e}")
            raise

    def search_by_image(
        self,
        image_path: str,
        n_results: int = 5,
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Search for similar garments using an image

        Args:
            image_path: Path to query image
            n_results: Number of results to return
            user_id: Filter by user ID

        Returns:
            List of matching garments
        """
        try:
            # Generate image embedding
            query_embedding = self.embeddings_service.encode_image(image_path)

            # Build where clause
            where_clause = {'user_id': user_id} if user_id else None

            # Query ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=n_results,
                where=where_clause
            )

            return self._parse_results(results)

        except Exception as e:
            print(f"Error searching by image: {e}")
            raise

    def get_garment(self, garment_id: str) -> Optional[Dict]:
        """Get a specific garment by ID"""
        try:
            result = self.collection.get(ids=[garment_id])

            if result['ids']:
                metadata = result['metadatas'][0]
                garment_data = json.loads(metadata.get('data', '{}'))
                
                # Asegurarse de que image_path esté en el garment_data
                if 'image_path' not in garment_data and 'image_path' in metadata:
                    garment_data['image_path'] = metadata['image_path']
                
                return garment_data

            return None

        except Exception as e:
            print(f"Error getting garment: {e}")
            return None

    def update_garment(self, garment_id: str, garment_data: Dict, image_path: str):
        """Update an existing garment"""
        try:
            # Delete old entry
            self.delete_garment(garment_id)

            # Add updated entry
            self.add_garment(garment_id, garment_data, image_path)

            print(f"Updated garment {garment_id}")

        except Exception as e:
            print(f"Error updating garment: {e}")
            raise

    def delete_garment(self, garment_id: str):
        """Delete a garment from ChromaDB"""
        try:
            self.collection.delete(ids=[garment_id])
            print(f"Deleted garment {garment_id}")

        except Exception as e:
            print(f"Error deleting garment: {e}")
            raise

    def get_all_garments(self, user_id: Optional[str] = None) -> List[Dict]:
        """Get all garments, optionally filtered by user"""
        try:
            where_clause = {'user_id': user_id} if user_id else None

            results = self.collection.get(
                where=where_clause,
                include=['metadatas']
            )

            garments = []
            for metadata in results.get('metadatas', []):
                garment_data = json.loads(metadata.get('data', '{}'))
                garments.append(garment_data)

            return garments

        except Exception as e:
            print(f"Error getting all garments: {e}")
            raise

    def _create_text_description(self, garment_data: Dict) -> str:
        """Create a text description from garment data for embedding"""
        parts = []

        if garment_data.get('name'):
            parts.append(garment_data['name'])

        if garment_data.get('category'):
            parts.append(f"Category: {garment_data['category']}")

        if garment_data.get('color'):
            parts.append(f"Color: {garment_data['color']}")

        if garment_data.get('style'):
            parts.append(f"Style: {garment_data['style']}")

        if garment_data.get('season'):
            parts.append(f"Season: {', '.join(garment_data['season'])}")

        if garment_data.get('description'):
            parts.append(garment_data['description'])

        if garment_data.get('tags'):
            parts.append(f"Tags: {', '.join(garment_data['tags'])}")

        return '. '.join(parts)

    def _parse_results(self, results: Dict) -> List[Dict]:
        """Parse ChromaDB query results"""
        parsed = []

        ids = results.get('ids', [[]])[0]
        metadatas = results.get('metadatas', [[]])[0]
        distances = results.get('distances', [[]])[0]

        for i, garment_id in enumerate(ids):
            metadata = metadatas[i]
            garment_data = json.loads(metadata.get('data', '{}'))
            garment_data['similarity_score'] = 1 - distances[i]  # Convert distance to similarity

            parsed.append(garment_data)

        return parsed


# Singleton instance
_chroma_service = None


def get_chroma_service() -> ChromaService:
    """Get singleton instance of ChromaService"""
    global _chroma_service
    if _chroma_service is None:
        _chroma_service = ChromaService()
    return _chroma_service
