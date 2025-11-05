from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
import uuid


@dataclass
class Garment:
    """Garment model representing a clothing item"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    name: str = ""
    category: str = ""  # e.g., 'top', 'bottom', 'dress', 'shoes', 'accessory'
    color: str = ""
    style: str = ""  # e.g., 'casual', 'formal', 'sporty'
    season: List[str] = field(default_factory=list)  # e.g., ['spring', 'summer']
    image_path: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        """Convert garment to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'category': self.category,
            'color': self.color,
            'style': self.style,
            'season': self.season,
            'image_path': self.image_path,
            'description': self.description,
            'tags': self.tags,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Garment':
        """Create garment from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            user_id=data.get('user_id', ''),
            name=data.get('name', ''),
            category=data.get('category', ''),
            color=data.get('color', ''),
            style=data.get('style', ''),
            season=data.get('season', []),
            image_path=data.get('image_path', ''),
            description=data.get('description', ''),
            tags=data.get('tags', []),
            metadata=data.get('metadata', {}),
            created_at=data.get('created_at', datetime.utcnow().isoformat()),
            updated_at=data.get('updated_at', datetime.utcnow().isoformat())
        )

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow().isoformat()


# Category constants
GARMENT_CATEGORIES = [
    'top',
    'bottom',
    'dress',
    'outerwear',
    'shoes',
    'accessory',
    'underwear',
    'activewear'
]

# Style constants
GARMENT_STYLES = [
    'casual',
    'formal',
    'business',
    'sporty',
    'streetwear',
    'bohemian',
    'vintage',
    'minimalist'
]

# Season constants
SEASONS = [
    'spring',
    'summer',
    'fall',
    'winter'
]
