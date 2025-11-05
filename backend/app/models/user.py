from dataclasses import dataclass, field
from typing import Dict, Optional
from datetime import datetime
import uuid


@dataclass
class User:
    """User model for wardrobe management"""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: str = ""
    preferences: Dict = field(default_factory=dict)  # Style preferences, favorite colors, etc.
    body_type: Optional[str] = None
    profile_image: Optional[str] = None  # For virtual try-on
    metadata: Dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        """Convert user to dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'preferences': self.preferences,
            'body_type': self.body_type,
            'profile_image': self.profile_image,
            'metadata': self.metadata,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """Create user from dictionary"""
        return cls(
            id=data.get('id', str(uuid.uuid4())),
            username=data.get('username', ''),
            email=data.get('email', ''),
            preferences=data.get('preferences', {}),
            body_type=data.get('body_type'),
            profile_image=data.get('profile_image'),
            metadata=data.get('metadata', {}),
            created_at=data.get('created_at', datetime.utcnow().isoformat()),
            updated_at=data.get('updated_at', datetime.utcnow().isoformat())
        )

    def update_timestamp(self):
        """Update the updated_at timestamp"""
        self.updated_at = datetime.utcnow().isoformat()
