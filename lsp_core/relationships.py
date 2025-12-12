
from dataclasses import dataclass, field
from typing import List, Set
from enum import Enum
from datetime import datetime

class RelationshipType(Enum):
    """Different kinds of relationships users form"""
    LEARNING_PARTNERSHIP = "learning_partnership"
    PROFESSIONAL_COLLABORATION = "professional_collaboration"
    MENTORSHIP = "mentorship"
    FRIENDSHIP = "friendship"
    CREATIVE_COLLABORATION = "creative_collaboration"
    RECREATIONAL_GROUP = "recreational_group"
    BUSINESS_RELATIONSHIP = "business_relationship"


@dataclass
class Relationship:
    """
    A connection between users that can span multiple relationship types.
    """
    relationship_id: str
    participants: List[str]  # User IDs
    relationship_types: Set[RelationshipType]
    initiated_date: datetime
    last_interaction: datetime
    interaction_frequency: float
    relationship_quality_score: float
