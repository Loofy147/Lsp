
"""
LSP Core Domain Models
- Foundational data structures for the Learning Social Platform.
- These models are production-ready and replace the original placeholders.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
from datetime import datetime

# ============================================================================
# Core Enums
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


class LanguageCapabilityDimension(Enum):
    """Specific capabilities for language learning - an example of a domain-specific dimension set"""
    VOCABULARY = "vocabulary"
    GRAMMAR = "grammar"
    LISTENING = "listening"
    SPEAKING = "speaking"
    READING = "reading"
    WRITING = "writing"
    PRONUNCIATION = "pronunciation"
    CULTURAL_KNOWLEDGE = "cultural_knowledge"


class FairnessMetric(Enum):
    """Different mathematical definitions of fairness"""
    STATISTICAL_PARITY = "statistical_parity"
    EQUAL_OPPORTUNITY = "equal_opportunity"
    EQUALIZED_ODDS = "equalized_odds"
    PREDICTIVE_PARITY = "predictive_parity"
    CALIBRATION = "calibration"

# ============================================================================
# Core User Profile Models
# ============================================================================

@dataclass
class UserPreferences:
    """User-configurable preferences and settings."""
    display_name: Optional[str] = None
    learning_goals: List[str] = field(default_factory=list)
    communication_style: str = "neutral"
    notification_frequency: str = "medium"

@dataclass
class CapabilityEstimate:
    """Bayesian estimate of a capability with uncertainty"""
    mean: float  # Point estimate
    variance: float  # Uncertainty
    confidence: float  # How much evidence we have

@dataclass
class InternalProfile:
    """
    The private laboratory where genuine learning happens.
    No social pressure, complete freedom to experiment and fail.
    """
    user_id: str
    activity_history: List['ActivityEvent'] = field(default_factory=list)
    capability_scores: Dict[CapabilityDimension, CapabilityEstimate] = field(default_factory=dict)
    learning_curves: Dict[ActivityDomain, 'LearningCurve'] = field(default_factory=dict)
    behavior_patterns: Dict[str, 'BehaviorPattern'] = field(default_factory=dict)
    preferences: UserPreferences = field(default_factory=UserPreferences)

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
    rated_contributions: List['RatedContribution'] = field(default_factory=list)
    achievement_timeline: List['Achievement'] = field(default_factory=list)
    peer_ratings: List['PeerRating'] = field(default_factory=list)

# ============================================================================
# Activity & Learning Models
# ============================================================================

@dataclass
class ActivityContext:
    """
    The circumstances surrounding an activity - critical for interpretation.
    """
    time_of_day: str
    day_of_week: str
    device_type: str
    location_type: str
    previous_activities: List[str] = field(default_factory=list)
    time_since_last_activity: float = 0.0
    current_goals: List[str] = field(default_factory=list)
    active_learning_paths: List[str] = field(default_factory=list)
    recent_achievements: List[str] = field(default_factory=list)
    collaborative: bool = False
    influenced_by_peers: bool = False
    external_context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ActivityEvent:
    """
    A single interaction or activity - the atomic unit of learning data.
    """
    event_id: str
    user_id: str
    timestamp: datetime
    domain: ActivityDomain
    activity_type: str
    action_data: Dict
    context: ActivityContext
    performance_metrics: Dict[str, float]
    capability_signals: Dict[CapabilityDimension, float]
    session_id: str
    sequence_position: int
    engagement_level: float
    frustration_indicators: List[str] = field(default_factory=list)
    flow_state_indicators: List[str] = field(default_factory=list)

@dataclass
class LearningCurve:
    """
    Tracks how a user progresses in a specific domain over time.
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
class LanguageAssessmentActivity:
    """A language learning activity that generates assessment data"""
    activity_id: str
    activity_type: str
    difficulty_level: float
    questions: List[Dict[str, Any]]
    dimensions_assessed: List[LanguageCapabilityDimension]

# ============================================================================
# Pattern & Reward Models
# ============================================================================

@dataclass
class BehaviorPattern:
    """
    A discovered pattern in user behavior that's meaningful for rewards.
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
class RewardConcept:
    """
    A type of reward that the algorithm has learned is meaningful.
    """
    concept_id: str
    concept_name: str
    concept_type: str
    target_pattern_id: str
    value_to_users: float
    eligibility_criteria: Dict[str, Any]
    delivery_mechanism: str
    social_visibility: str
    iterations: int
    user_feedback_score: float

@dataclass
class Achievement:
    """
    A specific instance of earning recognition.
    """
    achievement_id: str
    user_id: str
    timestamp: datetime
    reward_concept_id: str
    specific_instance: Dict
    earning_journey: List[str]
    user_satisfaction: Optional[float] = None
    subsequent_motivation_boost: Optional[float] = None

@dataclass
class Badge:
    """
    A badge represents recognition for a specific pattern of achievement.
    """
    badge_id: str
    name: str
    description: str
    icon_data: str
    rarity: float
    prestige_score: float

@dataclass
class PatternValidationResult:
    """Results of statistical validation for a discovered pattern"""
    pattern_id: str
    is_valid: bool
    temporal_stability_score: float
    distinctiveness_score: float
    predictive_validity: float
    sample_size: int
    confidence_level: float
    is_interpretable: bool
    human_readable_description: str

# ============================================================================
# Social & Economic Models
# ============================================================================

@dataclass
class PeerRating:
    """A rating given by one user to another."""
    rater_id: str
    rated_id: str
    timestamp: datetime
    ratings: Dict[str, float] # e.g., {"communication": 4.5, "reliability": 5.0}
    comments: Optional[str] = None

@dataclass
class RatedContribution:
    """A user contribution that has been rated by peers."""
    contribution_id: str
    user_id: str
    content: Any
    average_rating: float
    ratings: List[PeerRating] = field(default_factory=list)

@dataclass
class EconomicScenario:
    """Parameters for an economic scenario"""
    name: str
    num_users: int
    monthly_active_users: int
    ad_cpm: float
    ad_views_per_active_user_monthly: int
    ad_opt_out_rate: float
    avg_monthly_freelance_transactions: int
    avg_transaction_value: float
    platform_commission_rate: float
    premium_subscription_rate: float
    premium_monthly_price: float
    business_subscribers: int
    business_subscription_monthly: float
    credential_verifications_monthly: int
    verification_fee: float

@dataclass
class EconomicProjection:
    """Results of economic modeling"""
    scenario_name: str
    ad_revenue_monthly: float
    freelance_commission_monthly: float
    premium_subscription_revenue: float
    business_subscription_revenue: float
    credential_revenue_monthly: float
    total_revenue_monthly: float
    platform_share: float
    user_pool: float
    avg_per_user_monthly: float
    median_per_user_monthly: float
    is_viable: bool
    months_to_profitability: int
    runway_months: float

# ============================================================================
# Health & Safety Models (Fraud, Wellbeing, Fairness)
# ============================================================================

@dataclass
class FraudSignal:
    """A signal indicating potential fraudulent activity"""
    signal_type: str
    severity: float  # 0.0 to 1.0
    description: str
    evidence: Dict[str, Any]
    timestamp: datetime

@dataclass
class FraudAssessment:
    """Complete fraud risk assessment for an action"""
    is_suspicious: bool
    risk_score: float  # 0.0 to 1.0
    signals: List[FraudSignal]
    recommendation: str  # allow, review, block
    reasoning: str

@dataclass
class ActivityProfile:
    """Tracks a user's activity patterns for anomaly detection"""
    user_id: str
    last_activity_time: datetime
    activity_intervals: List[float] = field(default_factory=list)
    activity_times: List[datetime] = field(default_factory=list)
    hour_distribution: Dict[int, float] = field(default_factory=dict)

    def get_typical_activity_hours(self) -> Set[int]:
        return {h for h, f in self.hour_distribution.items() if f > 0.1}

@dataclass
class WellbeingConcern:
    """A detected wellbeing concern"""
    concern_type: str
    severity: float  # 0.0 to 1.0
    description: str
    detected_at: datetime
    recommendations: List[str]

@dataclass
class WellbeingAssessment:
    """Complete wellbeing assessment for a user"""
    user_id: str
    timestamp: datetime
    overall_score: float
    concerns: List[WellbeingConcern]
    positive_indicators: List[str]
    intervention_recommended: bool

@dataclass
class FairnessConfig:
    """Explicit fairness policy for the platform."""
    primary_metric: FairnessMetric = FairnessMetric.EQUAL_OPPORTUNITY
    protected_attributes: List[str] = field(default_factory=lambda: ["gender", "age", "location"])
    acceptable_disparity_threshold: float = 0.15
    policy_rationale: str = "..."

@dataclass
class FairnessAuditReport:
    """Results of a fairness audit"""
    metric_used: FairnessMetric
    protected_attribute: str
    groups_compared: List[str]
    group_metrics: Dict[str, Dict[str, float]]
    max_disparity: float
    min_disparity: float
    avg_disparity: float
    passes_threshold: bool
    threshold_used: float
    issues_found: List[str]
    recommendations: List[str]
    timestamp: datetime
