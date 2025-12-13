
"""
LSP Fairness Auditing System
- Provides a production-ready fairness auditor to ensure equitable treatment of users.
"""

from typing import Dict, List
from collections import defaultdict
import numpy as np
from datetime import datetime

from .models import (
    FairnessMetric,
    FairnessConfig,
    FairnessAuditReport,
    InternalProfile,
    Achievement,
)

# ============================================================================
# FAIRNESS METRICS & AUDITING
# ============================================================================

class FairnessAuditor:
    """
    Audits platform for fairness across protected groups.
    Implements multiple fairness metrics and generates actionable reports.
    """

    def __init__(self, config: FairnessConfig):
        self.config = config

    def audit_reward_distribution(
        self,
        users: List[InternalProfile],
        rewards_granted: Dict[str, List[Achievement]],
        user_demographics: Dict[str, Dict[str, str]]
    ) -> List[FairnessAuditReport]:
        """
        Comprehensive fairness audit of reward distribution.
        """
        reports = []
        for protected_attr in self.config.protected_attributes:
            report = self._audit_single_attribute(
                users,
                rewards_granted,
                user_demographics,
                protected_attr
            )
            reports.append(report)
        return reports

    def _audit_single_attribute(
        self,
        users: List[InternalProfile],
        rewards_granted: Dict[str, List[Achievement]],
        user_demographics: Dict[str, Dict[str, str]],
        protected_attribute: str
    ) -> FairnessAuditReport:
        """Audit fairness for a single protected attribute"""
        groups = self._group_users_by_attribute(users, user_demographics, protected_attribute)
        group_metrics = {
            group_id: self._calculate_group_metrics(group_users, rewards_granted, self.config.primary_metric)
            for group_id, group_users in groups.items()
        }

        disparities = self._calculate_disparities(group_metrics)
        max_disparity = max(disparities) if disparities else 0.0
        passes = max_disparity <= self.config.acceptable_disparity_threshold

        issues, recommendations = [], []
        if not passes:
            issues.append(f"Disparity of {max_disparity:.1%} exceeds threshold")
            recommendations.extend(self._generate_recommendations(protected_attribute, group_metrics))

        return FairnessAuditReport(
            metric_used=self.config.primary_metric,
            protected_attribute=protected_attribute,
            groups_compared=list(groups.keys()),
            group_metrics=group_metrics,
            max_disparity=max_disparity,
            min_disparity=min(disparities) if disparities else 0.0,
            avg_disparity=np.mean(disparities) if disparities else 0.0,
            passes_threshold=passes,
            threshold_used=self.config.acceptable_disparity_threshold,
            issues_found=issues,
            recommendations=recommendations,
            timestamp=datetime.now()
        )

    def _group_users_by_attribute(
        self,
        users: List[InternalProfile],
        demographics: Dict[str, Dict[str, str]],
        attribute: str
    ) -> Dict[str, List[InternalProfile]]:
        groups = defaultdict(list)
        for user in users:
            attr_value = demographics.get(user.user_id, {}).get(attribute, "unknown")
            groups[attr_value].append(user)
        return dict(groups)

    def _calculate_group_metrics(
        self,
        group_users: List[InternalProfile],
        rewards_granted: Dict[str, List[Achievement]],
        metric_type: FairnessMetric
    ) -> Dict[str, float]:
        if metric_type == FairnessMetric.EQUAL_OPPORTUNITY:
            return self._calculate_equal_opportunity_metrics(group_users, rewards_granted)
        elif metric_type == FairnessMetric.STATISTICAL_PARITY:
            return self._calculate_statistical_parity_metrics(group_users, rewards_granted)
        return {}

    def _calculate_equal_opportunity_metrics(
        self,
        group_users: List[InternalProfile],
        rewards_granted: Dict[str, List[Achievement]]
    ) -> Dict[str, float]:
        qualified_users = [u for u in group_users if self._is_qualified(u, 0.7)]
        if not qualified_users:
            return {"true_positive_rate": 0.0, "qualified_count": 0, "qualified_rewarded": 0}

        qualified_rewarded = sum(1 for u in qualified_users if u.user_id in rewards_granted and rewards_granted[u.user_id])
        tpr = qualified_rewarded / len(qualified_users)

        return {"true_positive_rate": tpr, "qualified_count": len(qualified_users), "qualified_rewarded": qualified_rewarded}

    def _calculate_statistical_parity_metrics(
        self,
        group_users: List[InternalProfile],
        rewards_granted: Dict[str, List[Achievement]]
    ) -> Dict[str, float]:
        if not group_users:
            return {"reward_rate": 0.0, "group_size": 0}

        rewarded = sum(1 for u in group_users if u.user_id in rewards_granted and rewards_granted[u.user_id])
        reward_rate = rewarded / len(group_users)

        return {"reward_rate": reward_rate, "group_size": len(group_users), "rewarded_count": rewarded}

    def _is_qualified(self, user: InternalProfile, threshold: float) -> bool:
        if not user.capability_scores:
            return False
        avg_capability = np.mean([est.mean for est in user.capability_scores.values()])
        return avg_capability >= threshold

    def _calculate_disparities(self, group_metrics: Dict[str, Dict[str, float]]) -> List[float]:
        disparities = []
        metric_key = next(iter(next(iter(group_metrics.values())).keys()))

        groups = list(group_metrics.keys())
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                metric1 = group_metrics[groups[i]][metric_key]
                metric2 = group_metrics[groups[j]][metric_key]
                disparities.append(abs(metric1 - metric2))

        return disparities

    def _generate_recommendations(
        self,
        protected_attribute: str,
        group_metrics: Dict[str, Dict[str, float]]
    ) -> List[str]:
        metric_key = next(iter(next(iter(group_metrics.values())).keys()))
        min_group = min(group_metrics, key=lambda g: group_metrics[g][metric_key])

        return [
            f"Group '{min_group}' has significantly lower {metric_key}.",
            "Review capability assessment for bias.",
            "Consider outreach to underserved groups."
        ]
