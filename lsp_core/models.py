
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from datetime import datetime

# ============================================================================
# DOMAIN MODELS - The foundational data structures
# ============================================================================

class ActivityDomain(Enum):
    """Different domains where users can engage and learn"""
    LANGUAGE_LEARNING = "language_learning"
    CREATIVE_WORK = "creative_work"
    FREELANCE_PROJECTS = "freelance_projects"
    SKILL_GAMES = "skill_games"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    PROBLEM_SOLVING = "problem_solving"
    SOCIAL_CONTRIBUTION = "social_contribution"
    PROFESSIONAL_WORK = "professional_work"


class CapabilityDimension(Enum):
    """Multidimensional aspects of user capabilities we track"""
    KNOWLEDGE_BREADTH = "knowledge_breadth"
    DOMAIN_DEPTH = "domain_depth"
    LEARNING_SPEED = "learning_speed"
    CREATIVITY = "creativity"
    ANALYTICAL_THINKING = "analytical_thinking"
    COMMUNICATION = "communication"
    COLLABORATION = "collaboration"
    PERSISTENCE = "persistence"
    ADAPTABILITY = "adaptability"
    RELIABILITY = "reliability"
    EMOTIONAL_INTELLIGENCE = "emotional_intelligence"
    PATTERN_RECOGNITION = "pattern_recognition"
    RISK_TOLERANCE = "risk_tolerance"

@dataclass
class UserPreferences:
    """Placeholder for user preferences."""
    display_name: Optional[str] = None

@dataclass
class TemporalPattern:
    """Placeholder for temporal patterns."""
    pass

@dataclass
class ExternalDataSource:
    """Placeholder for external data sources."""
    pass

@dataclass
class RatedContribution:
    """Placeholder for rated contributions."""
    pass

@dataclass
class PeerRating:
    """Placeholder for peer ratings."""
    pass

@dataclass
class EligibilityModel:
    """Placeholder for eligibility models."""
    pass

@dataclass
class JourneySummary:
    """Placeholder for journey summaries."""
    pass

@dataclass
class InternalProfile:
    """
    The private laboratory where genuine learning happens.
    No social pressure, complete freedom to experiment and fail.
    """
    user_id: str
    activity_history: List['ActivityEvent'] = field(default_factory=list)
    capability_scores: Dict[CapabilityDimension, float] = field(default_factory=dict)
    learning_curves: Dict[ActivityDomain, 'LearningCurve'] = field(default_factory=dict)
    behavior_patterns: Dict[str, 'BehaviorPattern'] = field(default_factory=dict)
    preferences: Optional[UserPreferences] = None
    engagement_rhythms: Optional[TemporalPattern] = None
    external_connections: Dict[str, ExternalDataSource] = field(default_factory=dict)


@dataclass
class SocialProfile:
    """
    The public showcase of achievements and recognition.
    Carefully curated to show growth without exposing vulnerability.
    """
    user_id: str
    display_name: str
    badges: List['Badge'] = field(default_factory=list)
    ranks: Dict[str, int] = field(default_factory=dict)
    public_scores: Dict[str, float] = field(default_factory=dict)
    social_capital: float = 0.0
    reputation_score: float = 0.0
    rated_contributions: List[RatedContribution] = field(default_factory=list)
    achievement_timeline: List['Achievement'] = field(default_factory=list)
    peer_ratings: List[PeerRating] = field(default_factory=list)


@dataclass
class ActivityEvent:
    """
    A single interaction or activity - the atomic unit of learning data.
    Each event captures rich context about what happened and why.
    """
    event_id: str
    user_id: str
    timestamp: datetime
    domain: ActivityDomain
    activity_type: str
    action_data: Dict
    context: 'ActivityContext'
    performance_metrics: Dict[str, float]
    capability_signals: Dict[CapabilityDimension, float]
    session_id: str
    sequence_position: int
    engagement_level: float
    frustration_indicators: List[str]
    flow_state_indicators: List[str]


@dataclass
class ActivityContext:
    """
    The circumstances surrounding an activity - critical for interpretation.
    Same action in different contexts reveals different things about the user.
    """
    time_of_day: str
    day_of_week: str
    device_type: str
    location_type: str
    previous_activities: List[str]
    time_since_last_activity: float
    current_goals: List[str]
    active_learning_paths: List[str]
    recent_achievements: List[str]
    collaborative: bool
    influenced_by_peers: bool
    external_context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LearningCurve:
    """
    Tracks how a user progresses in a specific domain over time.
    Not just final achievement but the shape of the journey matters.
    """
    domain: ActivityDomain
    start_date: datetime
    progress_points: List[Tuple[datetime, float]] = field(default_factory=list)
    learning_velocity: float = 0.0
    consistency_score: float = 0.0
    plateau_periods: List[Tuple[datetime, datetime]] = field(default_factory=list)
    breakthrough_moments: List[datetime] = field(default_factory=list)
    learning_style_indicators: Dict[str, float] = field(default_factory=dict)


@dataclass
class BehaviorPattern:
    """
    A discovered pattern in user behavior that's meaningful for rewards.
    These emerge from clustering and analysis, not predefined categories.
    """
    pattern_id: str
    pattern_name: str
    description: str
    characteristic_behaviors: List[str]
    capability_profile: Dict[CapabilityDimension, float]
    temporal_signature: Dict[str, float]
    strength: float
    consistency: float
    triggering_contexts: List[str]


@dataclass
class Badge:
    """
    A badge represents recognition for a specific pattern of achievement.
    Can be standard or algorithmically generated.
    """
    badge_id: str
    name: str
    description: str
    icon_data: str
    recognized_pattern: BehaviorPattern
    required_capabilities: Dict[CapabilityDimension, float]
    rarity: float
    algorithmically_generated: bool
    creation_date: datetime
    prestige_score: float


@dataclass
class RewardConcept:
    """
    A type of reward that the algorithm has learned is meaningful.
    These can be traditional (badges, points) or newly synthesized.
    """
    concept_id: str
    concept_name: str
    concept_type: str
    target_pattern: BehaviorPattern
    value_to_users: float
    eligibility_model: EligibilityModel
    delivery_mechanism: str
    social_visibility: str
    iterations: int
    user_feedback_score: float


@dataclass
class Achievement:
    """

    A specific instance of earning recognition.
    Captures what was achieved and the journey to get there.
    """
    achievement_id: str
    user_id: str
    timestamp: datetime
    reward: RewardConcept
    specific_instance: Dict
    earning_journey: JourneySummary
    user_satisfaction: Optional[float] = None
    subsequent_motivation_boost: Optional[float] = None
