
from dataclasses import dataclass, field
from typing import Dict, List
from enum import Enum
from .models import InternalProfile, ActivityEvent, LearningCurve

# ============================================================================
# ECONOMIC SYSTEM - Fair revenue generation and distribution
# ============================================================================

class RevenueStream(Enum):
    """Different ways the platform generates revenue"""
    CONTEXTUAL_ADVERTISING = "contextual_advertising"
    FREELANCE_COMMISSION = "freelance_commission"
    BUSINESS_SUBSCRIPTIONS = "business_subscriptions"
    CREDENTIAL_VERIFICATION = "credential_verification"
    PREMIUM_FEATURES = "premium_features"
    MARKETPLACE_FEES = "marketplace_fees"
    EVENT_BOOKING_FEES = "event_booking_fees"


@dataclass
class RevenueAllocation:
    """
    How revenue from each stream is allocated between platform and users.
    These allocations should be transparent and fair.
    """
    stream: RevenueStream
    platform_percentage: float
    direct_contributor_percentage: float
    indirect_contributor_pool_percentage: float
    distribution_period: str = "monthly"


@dataclass
class ContributionScore:
    """
    Multi-dimensional measure of how a user creates value for the ecosystem.
    This determines their share of indirect revenue pools.
    """
    user_id: str
    period: str
    paid_work_completed: float = 0.0
    services_provided: float = 0.0
    content_created: float = 0.0
    behavioral_data_quality: float = 0.0
    peer_rating_accuracy: float = 0.0
    mentorship_impact: float = 0.0
    community_health_contribution: float = 0.0
    feedback_quality: float = 0.0
    bug_reports: float = 0.0
    feature_suggestions_adopted: float = 0.0
    total_contribution: float = 0.0

# Placeholder classes for data structures that would be defined elsewhere
@dataclass
class CompletedWork:
    worker_id: str
    payment: float

@dataclass
class AdTargetedUser:
    user_id: str
    ad_value_weight: float

@dataclass
class Project:
    payment_amount: float
    client_satisfaction: float
    is_repeat_client: bool
    skill_complexity_factor: float

@dataclass
class MentoringActivity:
    mentee_id: str
    timestamp: str
    duration_minutes: int

class ContributionCalculator:
    """
    Calculates how much value each user creates for the ecosystem.
    """
    def calculate_score(self, user: InternalProfile, period: str) -> ContributionScore:
        """
        Comprehensive assessment of user's value contribution.
        """
        score = ContributionScore(user_id=user.user_id, period=period)

        score.paid_work_completed = self._calculate_work_value(user, period)
        score.services_provided = self._calculate_service_value(user, period)
        score.content_created = self._calculate_content_value(user, period)
        score.behavioral_data_quality = self._assess_data_quality(user, period)
        score.peer_rating_accuracy = self._assess_rating_quality(user, period)
        score.mentorship_impact = self._assess_mentorship_impact(user, period)
        score.community_health_contribution = self._assess_social_impact(user, period)
        score.feedback_quality = self._assess_feedback_value(user, period)
        score.total_contribution = self._aggregate_contributions(score)

        return score

    # Placeholder methods for functionality that would be built out
    def _calculate_work_value(self, user: InternalProfile, period: str) -> float: return 0.0
    def _calculate_service_value(self, user: InternalProfile, period: str) -> float: return 0.0
    def _calculate_content_value(self, user: InternalProfile, period: str) -> float: return 0.0
    def _assess_data_quality(self, user: InternalProfile, period: str) -> float: return 0.0
    def _assess_rating_quality(self, user: InternalProfile, period: str) -> float: return 0.0
    def _assess_mentorship_impact(self, user: InternalProfile, period: str) -> float: return 0.0
    def _assess_social_impact(self, user: InternalProfile, period: str) -> float: return 0.0
    def _assess_feedback_value(self, user: InternalProfile, period: str) -> float: return 0.0
    def _aggregate_contributions(self, score: ContributionScore) -> float:
        return sum([
            score.paid_work_completed, score.services_provided, score.content_created,
            score.behavioral_data_quality, score.peer_rating_accuracy, score.mentorship_impact,
            score.community_health_contribution, score.feedback_quality
        ])

class RevenueDistributionEngine:
    """
    Calculates fair distribution of revenue to users based on contribution.
    """
    def __init__(self):
        self.allocations: Dict[RevenueStream, RevenueAllocation] = {}
        self.contribution_calculator = ContributionCalculator()

    def calculate_period_distribution(
        self, period: str, revenue_by_stream: Dict[RevenueStream, float], all_users: List[InternalProfile]
    ) -> Dict[str, float]:
        """
        Calculate how much each user should receive for this period.
        """
        user_earnings: Dict[str, float] = {}

        for stream, revenue in revenue_by_stream.items():
            allocation = self.allocations.get(stream)
            if not allocation: continue

            # Direct contributor percentage
            direct_share = revenue * allocation.direct_contributor_percentage
            direct_earnings = self._distribute_direct_contributions(stream, direct_share, period)

            # Indirect contributor pool
            indirect_share = revenue * allocation.indirect_contributor_pool_percentage
            indirect_earnings = self._distribute_indirect_contributions(indirect_share, all_users, period)

            # Combine earnings
            for user_id, amount in {**direct_earnings, **indirect_earnings}.items():
                user_earnings[user_id] = user_earnings.get(user_id, 0.0) + amount

        return user_earnings

    def _distribute_direct_contributions(
        self, stream: RevenueStream, pool: float, period: str
    ) -> Dict[str, float]:
        # Placeholder for complex logic
        return {}

    def _distribute_indirect_contributions(
        self, pool: float, all_users: List[InternalProfile], period: str
    ) -> Dict[str, float]:
        """
        Distribute indirect contribution pool based on contribution scores.
        """
        contribution_scores = {
            user.user_id: self.contribution_calculator.calculate_score(user, period)
            for user in all_users
        }

        total_contribution = sum(s.total_contribution for s in contribution_scores.values())
        if total_contribution == 0: return {}

        earnings: Dict[str, float] = {}
        for user_id, score in contribution_scores.items():
            share = (score.total_contribution / total_contribution) * pool
            earnings[user_id] = share

        return earnings
