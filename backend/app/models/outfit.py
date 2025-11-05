from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid


@dataclass
class Outfit:
    """Outfit model representing a combination of garments"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    name: str = ""
    garment_ids: List[str] = field(default_factory=list)
    occasion: str = ""  # e.g., 'casual', 'work', 'party', 'date'
    season: str = ""
    style: str = ""
    description: str = ""
    rating: Optional[int] = None  # User rating 1-5
    tags: List[str] = field(default_factory=list)
    generated_image_path: Optional[str] = None  # Virtual try-on result
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        """Convert outfit to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'garment_ids': self.garment_ids,
            'occasion': self.occasion,
            'season': self.season,
            'style': self.style,
            'description': self.description,
            'rating': self.rating,
            'tags': self.tags,
            'generated_image_path': self.generated_image_path,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Outfit':
        """Create outfit from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            user_id=data.get('user_id', ''),
            name=data.get('name', ''),
            garment_ids=data.get('garment_ids', []),
            occasion=data.get('occasion', ''),
            season=data.get('season', ''),
            style=data.get('style', ''),
            description=data.get('description', ''),
            rating=data.get('rating'),
            tags=data.get('tags', []),
            generated_image_path=data.get('generated_image_path'),
            metadata=data.get('metadata', {}),
            created_at=data.get('created_at', datetime.utcnow().isoformat()),
            updated_at=data.get('updated_at', datetime.utcnow().isoformat())
        )

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow().isoformat()

    def add_garment(self, garment_id: str):
        """Add a garment to the outfit"""
        if garment_id not in self.garment_ids:
            self.garment_ids.append(garment_id)
            self.update_timestamp()

    def remove_garment(self, garment_id: str):
        """Remove a garment from the outfit"""
        if garment_id in self.garment_ids:
            self.garment_ids.remove(garment_id)
            self.update_timestamp()


# Occasion constants
OCCASIONS = [
    'casual',
    'work',
    'business',
    'party',
    'date',
    'wedding',
    'sports',
    'travel',
    'beach',
    'formal_event'
]
