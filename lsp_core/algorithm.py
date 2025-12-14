
"""
LSP Core Algorithms
- Production-ready implementations of the core LSP algorithms.
- Replaces the original placeholder classes.
"""

from .models import (
    ActivityEvent,
    InternalProfile,
    BehaviorPattern,
    CapabilityDimension,
    LanguageCapabilityDimension,
    LanguageAssessmentActivity,
    CapabilityEstimate,
    PatternValidationResult,
    WellbeingAssessment,
    WellbeingConcern,
    FraudAssessment,
    ActivityProfile,
    FraudSignal,
)
from typing import Dict, List, Optional, Set, Tuple, Any
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import hashlib
import json
from sklearn.cluster import KMeans

# ============================================================================
# 1. FRAUD DETECTION & SECURITY SYSTEM
# ============================================================================

class FraudDetector:
    """
    Multi-layered fraud detection using behavioral analysis,
    graph analysis, and statistical anomaly detection.
    """

    def __init__(self):
        self.user_activity_profiles: Dict[str, ActivityProfile] = {}
        self.social_graph: Dict[str, Set[str]] = defaultdict(set)
        self.rating_history: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        self.device_fingerprints: Dict[str, Set[str]] = defaultdict(set)

    def assess_activity_authenticity(
        self,
        user_id: str,
        activity: ActivityEvent,
        context: Dict[str, Any]
    ) -> FraudAssessment:
        signals = []

        velocity_signal = self._check_velocity(user_id, activity)
        if velocity_signal:
            signals.append(velocity_signal)

        regularity_signal = self._check_pattern_regularity(user_id, activity)
        if regularity_signal:
            signals.append(regularity_signal)

        biometric_signal = self._check_behavioral_biometrics(activity, context)
        if biometric_signal:
            signals.append(biometric_signal)

        temporal_signal = self._check_temporal_anomaly(user_id, activity)
        if temporal_signal:
            signals.append(temporal_signal)

        device_signal = self._check_device_fingerprint(user_id, context)
        if device_signal:
            signals.append(device_signal)

        risk_score = self._calculate_risk_score(signals)

        if risk_score > 0.8:
            recommendation = "block"
        elif risk_score > 0.5:
            recommendation = "review"
        else:
            recommendation = "allow"

        return FraudAssessment(
            is_suspicious=risk_score > 0.5,
            risk_score=risk_score,
            signals=signals,
            recommendation=recommendation,
            reasoning=""
        )

    def _check_velocity(
        self,
        user_id: str,
        activity: ActivityEvent
    ) -> Optional[FraudSignal]:
        profile = self.user_activity_profiles.get(user_id)
        if not profile:
            return None

        time_since_last = (activity.timestamp - profile.last_activity_time).total_seconds()

        min_time_required = 1

        if time_since_last < min_time_required * 0.5:
            return FraudSignal(
                signal_type="velocity_violation",
                severity=0.7,
                description=f"Activity completed in {time_since_last}s",
                evidence={},
                timestamp=datetime.now()
            )

        return None

    def _check_pattern_regularity(
        self,
        user_id: str,
        activity: ActivityEvent
    ) -> Optional[FraudSignal]:
        profile = self.user_activity_profiles.get(user_id)
        if not profile or len(profile.activity_intervals) < 10:
            return None

        intervals = profile.activity_intervals[-20:]
        cv = np.std(intervals) / np.mean(intervals) if np.mean(intervals) > 0 else 0

        if cv < 0.15:
            return FraudSignal(
                signal_type="pattern_too_regular",
                severity=0.6,
                description=f"Activity timing too regular (CV={cv:.3f})",
                evidence={},
                timestamp=datetime.now()
            )

        return None

    def _check_behavioral_biometrics(
        self,
        activity: ActivityEvent,
        context: Dict[str, Any]
    ) -> Optional[FraudSignal]:
        mouse_data = context.get('mouse_movements', [])
        typing_data = context.get('typing_pattern', {})

        signals_found = []

        if mouse_data and len(mouse_data) > 5:
            straightness = self._calculate_path_straightness(mouse_data)
            if straightness > 0.95:
                signals_found.append("mouse_too_straight")

        if typing_data:
            key_intervals = typing_data.get('key_intervals', [])
            if key_intervals and len(key_intervals) > 10:
                typing_cv = np.std(key_intervals) / np.mean(key_intervals)
                if typing_cv < 0.2:
                    signals_found.append("typing_too_regular")

        if signals_found:
            return FraudSignal(
                signal_type="biometric_anomaly",
                severity=0.5,
                description=f"Unusual behavioral biometrics: {', '.join(signals_found)}",
                evidence={"anomalies": signals_found},
                timestamp=datetime.now()
            )

        return None

    def _check_temporal_anomaly(
        self,
        user_id: str,
        activity: ActivityEvent
    ) -> Optional[FraudSignal]:
        profile = self.user_activity_profiles.get(user_id)
        if not profile or len(profile.activity_times) < 20:
            return None

        typical_hours = profile.get_typical_activity_hours()
        current_hour = activity.timestamp.hour

        if current_hour not in typical_hours:
            hour_frequency = profile.hour_distribution.get(current_hour, 0)
            if hour_frequency < 0.05:
                return FraudSignal(
                    signal_type="temporal_anomaly",
                    severity=0.4,
                    description=f"Activity at unusual hour {current_hour}:00",
                    evidence={},
                    timestamp=datetime.now()
                )

        return None

    def _check_device_fingerprint(
        self,
        user_id: str,
        context: Dict[str, Any]
    ) -> Optional[FraudSignal]:
        device_fingerprint = self._generate_device_fingerprint(context)
        known_devices = self.device_fingerprints.get(user_id, set())

        if device_fingerprint not in known_devices:
            users_on_device = sum(1 for devices in self.device_fingerprints.values() if device_fingerprint in devices)

            if users_on_device > 3:
                return FraudSignal(
                    signal_type="device_sharing",
                    severity=0.8,
                    description=f"Device shared by {users_on_device} accounts",
                    evidence={},
                    timestamp=datetime.now()
                )

            if len(known_devices) > 0:
                return FraudSignal(
                    signal_type="new_device",
                    severity=0.3,
                    description="Activity from new device",
                    evidence={},
                    timestamp=datetime.now()
                )

        self.device_fingerprints[user_id].add(device_fingerprint)
        return None

    def _calculate_risk_score(self, signals: List[FraudSignal]) -> float:
        if not signals:
            return 0.0

        sorted_signals = sorted(signals, key=lambda s: s.severity, reverse=True)
        weights = [1.0, 0.7, 0.5, 0.3, 0.2]

        total_score = sum(s.severity * w for s, w in zip(sorted_signals, weights))
        total_weight = sum(weights[:len(sorted_signals)])

        return min(total_score / total_weight if total_weight > 0 else 0.0, 1.0)

    def _generate_device_fingerprint(self, context: Dict[str, Any]) -> str:
        fingerprint_data = {k: context.get(k, '') for k in ['user_agent', 'screen_resolution', 'timezone']}
        fingerprint_string = json.dumps(fingerprint_data, sort_keys=True)
        return hashlib.sha256(fingerprint_string.encode()).hexdigest()

    def _calculate_path_straightness(self, mouse_movements: List[Tuple[int, int]]) -> float:
        if len(mouse_movements) < 3:
            return 0.5

        path_length = sum(np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) for p1, p2 in zip(mouse_movements, mouse_movements[1:]))
        direct_distance = np.sqrt((mouse_movements[-1][0]-mouse_movements[0][0])**2 + (mouse_movements[-1][1]-mouse_movements[0][1])**2)

        return direct_distance / path_length if path_length > 0 else 0.5

# ============================================================================
# 2. CAPABILITY ASSESSMENT
# ============================================================================

class MultiDimensionalAssessor:
    """
    A generic, configurable capability assessor that uses Bayesian updating
    to estimate user capabilities from activity performance.
    """

    def __init__(self, dimensions: List[Enum]):
        self.dimensions = dimensions
        self.capability_estimates: Dict[Enum, CapabilityEstimate] = {
            dim: CapabilityEstimate(mean=0.3, variance=0.2, confidence=0.1)
            for dim in self.dimensions
        }

    def assess_from_activity(
        self,
        activity: Any, # Using Any to be generic, could be a protocol
        performance_signals: Dict[str, float],
        dimensions_assessed: List[Enum]
    ) -> Dict[Enum, float]:
        """
        Updates capability estimates based on performance in an activity.

        Args:
            activity: The activity object, containing context like difficulty.
            performance_signals: A dict of performance metrics (e.g., {'accuracy': 0.8, 'speed': 0.9}).
            dimensions_assessed: A list of the capability dimensions this activity targets.

        Returns:
            A dictionary of the updated capability mean scores.
        """
        updated_estimates = {}

        for dimension in dimensions_assessed:
            # This logic assumes a simple signal extraction; could be made more configurable
            signal = self._extract_signal(performance_signals)
            difficulty = getattr(activity, 'difficulty_level', 0.5)

            updated = self._bayesian_update(self.capability_estimates[dimension], signal, difficulty)
            self.capability_estimates[dimension] = updated
            updated_estimates[dimension] = updated.mean

        return updated_estimates

    def _extract_signal(self, performance: Dict[str, float]) -> float:
        """A simple, generic way to get a single signal from performance data."""
        if not performance:
            return 0.5
        # Default to averaging all performance metrics
        return np.mean(list(performance.values()))

    def _bayesian_update(
        self,
        prior: CapabilityEstimate,
        signal: float,
        difficulty: float
    ) -> CapabilityEstimate:
        """Updates a prior belief with a new signal."""
        # Confidence in the signal is influenced by activity difficulty
        signal_confidence = 0.3 + (difficulty * 0.4)

        prior_weight = prior.confidence
        signal_weight = signal_confidence
        total_weight = prior_weight + signal_weight

        if total_weight == 0:
            return prior

        # Weighted average for the new mean
        new_mean = ((prior.mean * prior_weight + signal * signal_weight) / total_weight)

        # Reduce variance and increase confidence
        new_variance = prior.variance * (1 - signal_confidence * 0.1)
        new_confidence = min(prior.confidence + signal_confidence * 0.1, 0.95)

        return CapabilityEstimate(mean=new_mean, variance=new_variance, confidence=new_confidence)

class LanguageCapabilityAssessor(MultiDimensionalAssessor):
    """
    A specialized assessor for language learning that builds upon the generic
    MultiDimensionalAssessor, providing domain-specific logic for signal extraction.
    """

    def __init__(self, target_language: str):
        super().__init__(dimensions=list(LanguageCapabilityDimension))
        self.target_language = target_language

    def assess(
        self,
        activity: LanguageAssessmentActivity,
        user_responses: List[Dict[str, Any]]
    ) -> Dict[LanguageCapabilityDimension, float]:
        """
        Specialized assessment method for language activities. It calculates
        performance and then uses the generic assessment logic from the parent class.
        """
        performance = self._calculate_performance(user_responses)

        # Call the generic parent method with the extracted signals
        return super().assess_from_activity(
            activity=activity,
            performance_signals=performance,
            dimensions_assessed=activity.dimensions_assessed
        )

    def _calculate_performance(self, user_responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculates accuracy and speed from user responses."""
        if not user_responses:
            return {'accuracy': 0.0, 'speed': 0.0}

        accuracy = sum(1 for r in user_responses if r.get('correct', False)) / len(user_responses)
        total_time = sum(r.get('time_taken', 0) for r in user_responses)

        # Avoid division by zero for speed
        speed = (len(user_responses) / (total_time / 60)) if total_time > 0 else 0

        return {'accuracy': accuracy, 'speed': speed}

    def _extract_signal(self, performance: Dict[str, float]) -> float:
        """
        Overrides the generic signal extraction to use a domain-specific rule:
        accuracy is the primary signal for language learning.
        """
        return performance.get('accuracy', 0.5)

# ============================================================================
# 3. PATTERN VALIDATION
# ============================================================================

class PatternValidator:
    """
    Rigorously validates discovered behavior patterns.
    """

    def __init__(
        self,
        min_sample_size: int = 30,
        required_confidence: float = 0.95,
        temporal_window_days: int = 30
    ):
        self.min_sample_size = min_sample_size
        self.required_confidence = required_confidence
        self.temporal_window_days = temporal_window_days

    def validate_pattern(
        self,
        pattern: BehaviorPattern,
        cluster_users: List[InternalProfile],
        all_users: List[InternalProfile]
    ) -> PatternValidationResult:
        if len(cluster_users) < self.min_sample_size:
            return PatternValidationResult(
                pattern_id=pattern.pattern_id,
                is_valid=False,
                human_readable_description="Insufficient sample size",
                temporal_stability_score=0,
                distinctiveness_score=0,
                predictive_validity=0,
                sample_size=len(cluster_users),
                confidence_level=0,
                is_interpretable=False
            )

        stability_score = self._test_temporal_stability(cluster_users)
        distinctiveness_score = self._test_distinctiveness(cluster_users, all_users)
        predictive_score = self._test_predictive_validity(cluster_users)
        is_interpretable, description = self._test_interpretability(pattern)

        is_valid = (
            stability_score > 0.7 and
            distinctiveness_score > 0.8 and
            predictive_score > 0.6 and
            is_interpretable
        )

        return PatternValidationResult(
            pattern_id=pattern.pattern_id,
            is_valid=is_valid,
            temporal_stability_score=stability_score,
            distinctiveness_score=distinctiveness_score,
            predictive_validity=predictive_score,
            sample_size=len(cluster_users),
            confidence_level=self.required_confidence,
            is_interpretable=is_interpretable,
            human_readable_description=description
        )

    def _test_temporal_stability(self, cluster_users: List[InternalProfile]) -> float:
        """
        Tests if the pattern is consistent over time.
        A simple check: is user activity consistent in two halves of their history?
        """
        if not cluster_users:
            return 0.0

        stability_scores = []
        for user in cluster_users:
            history = sorted(user.activity_history, key=lambda x: x.timestamp)
            if len(history) < 2:
                continue

            midpoint = len(history) // 2
            first_half_engagement = np.mean([a.engagement_level for a in history[:midpoint]])
            second_half_engagement = np.mean([a.engagement_level for a in history[midpoint:]])

            # Score is 1.0 minus the normalized difference
            stability = 1.0 - abs(first_half_engagement - second_half_engagement)
            stability_scores.append(stability)

        return np.mean(stability_scores) if stability_scores else 0.0

    def _test_distinctiveness(self, cluster_users: List[InternalProfile], all_users: List[InternalProfile]) -> float:
        """
        Tests if the user cluster is meaningfully different from the general population.
        """
        if not cluster_users or not all_users:
            return 0.0

        # Compare the average 'creativity' capability of the cluster vs. general population
        cluster_creativity = np.mean([
            u.capability_scores.get(CapabilityDimension.CREATIVITY, CapabilityEstimate(mean=0.0)).mean
            for u in cluster_users
        ])

        general_creativity = np.mean([
            u.capability_scores.get(CapabilityDimension.CREATIVITY, CapabilityEstimate(mean=0.0)).mean
            for u in all_users
        ])

        # Score is the normalized difference
        return abs(cluster_creativity - general_creativity)

    def _test_predictive_validity(self, cluster_users: List[InternalProfile]) -> float:
        """
        Tests if the pattern predicts a positive future outcome, e.g., continued engagement.
        """
        if not cluster_users:
            return 0.0

        # A simple predictive test: do users in this cluster maintain or increase engagement?
        engagement_trends = []
        for user in cluster_users:
            history = sorted(user.activity_history, key=lambda x: x.timestamp)
            if len(history) < 10: # Need sufficient history
                continue

            recent_engagement = np.mean([a.engagement_level for a in history[-5:]])
            past_engagement = np.mean([a.engagement_level for a in history[:5]])

            # Positive trend is good
            engagement_trends.append(1.0 if recent_engagement >= past_engagement else 0.0)

        return np.mean(engagement_trends) if engagement_trends else 0.0

    def _test_interpretability(self, pattern: BehaviorPattern) -> Tuple[bool, str]:
        """
        Generates a human-readable description for the pattern.
        """
        # This can be made more sophisticated, but for now, we'll use the generated name
        description = pattern.description or f"A pattern related to {pattern.pattern_name}"
        is_interpretable = bool(description)
        return is_interpretable, description

# ============================================================================
# 4. PATTERN DISCOVERY ENGINE
# ============================================================================

class PatternDiscoveryEngine:
    """
    Discovers meaningful patterns in user behavior using clustering.
    """
    def __init__(self, n_clusters: int = 5):
        self.clusterer = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)

    def discover_patterns(self, users: List[InternalProfile]) -> List[BehaviorPattern]:
        """
        Analyzes user data to find and define behavior patterns.
        """
        if not users or len(users) < self.clusterer.n_clusters:
            return []

        vectors = self._create_behavior_vectors(users)
        cluster_labels = self.clusterer.fit_predict(vectors)

        patterns = []
        for i in range(self.clusterer.n_clusters):
            cluster_users = [users[j] for j, label in enumerate(cluster_labels) if label == i]
            if cluster_users:
                pattern = self._extract_pattern_from_cluster(i, cluster_users)
                patterns.append(pattern)

        return patterns

    def _create_behavior_vectors(self, users: List[InternalProfile]) -> np.ndarray:
        """
        Creates a richer numerical vector representation of each user's behavior,
        including capabilities, engagement, and activity metrics.
        """

        # Use all available capability dimensions for a comprehensive profile
        dimensions = list(CapabilityDimension)

        vectors = []
        for user in users:
            # 1. Capability scores
            capability_vector = [
                user.capability_scores.get(dim, CapabilityEstimate(mean=0.0, variance=0.0, confidence=0.0)).mean
                for dim in dimensions
            ]

            # 2. Activity and engagement metrics
            if user.activity_history:
                sorted_history = sorted(user.activity_history, key=lambda x: x.timestamp)

                # Engagement
                avg_engagement = np.mean([a.engagement_level for a in sorted_history])

                # Activity Count
                activity_count = len(sorted_history)

                # Recency
                last_activity_date = sorted_history[-1].timestamp
                days_since_last_activity = (datetime.now() - last_activity_date).days

                # Frequency
                first_activity_date = sorted_history[0].timestamp
                total_duration_days = (last_activity_date - first_activity_date).days
                activities_per_day = activity_count / (total_duration_days + 1)  # Add 1 to avoid division by zero

            else:
                avg_engagement = 0.0
                activity_count = 0.0
                days_since_last_activity = 365.0  # High value for inactive users
                activities_per_day = 0.0

            # 3. Combine into a single feature vector
            feature_vector = capability_vector + [
                avg_engagement,
                activity_count,
                days_since_last_activity,
                activities_per_day
            ]
            vectors.append(feature_vector)

        # Normalize the vectors for clustering
        vectors_array = np.array(vectors)
        if vectors_array.shape[0] > 0:
            # Add epsilon for stability
            vectors_array = (vectors_array - vectors_array.mean(axis=0)) / (vectors_array.std(axis=0) + 1e-6)

        return vectors_array

    def _extract_pattern_from_cluster(self, cluster_id: int, users: List[InternalProfile]) -> BehaviorPattern:
        """
        Generates a human-readable definition of a behavior pattern from a user cluster.
        """
        # Simplified description based on the dominant capability in the cluster
        avg_capabilities = defaultdict(float)
        for user in users:
            for dim, estimate in user.capability_scores.items():
                avg_capabilities[dim] += estimate.mean

        if avg_capabilities:
            dominant_capability = max(avg_capabilities, key=avg_capabilities.get)
            description = f"Users who are strong in {dominant_capability.value}"
        else:
            description = "General activity pattern"
            dominant_capability = None

        return BehaviorPattern(
            pattern_id=f"cluster_{cluster_id}",
            pattern_name=f"Pattern {cluster_id}",
            description=description,
            characteristic_behaviors=[],
            capability_profile={dominant_capability: avg_capabilities[dominant_capability] / len(users)} if dominant_capability else {},
            temporal_signature={},
            strength=0.0,
            consistency=0.0,
            triggering_contexts=[]
        )

# ============================================================================
# 5. WELLBEING MONITORING
# ============================================================================

class WellbeingMonitor:
    """
    Monitors user engagement for unhealthy patterns.
    """

    def __init__(self):
        self.max_daily_hours = 4.0

    def assess_wellbeing(
        self,
        user: InternalProfile,
        recent_days: int = 7
    ) -> WellbeingAssessment:
        concerns = []

        cutoff = datetime.now() - timedelta(days=recent_days)
        recent_activities = [a for a in user.activity_history if a.timestamp > cutoff]

        excessive_time = self._check_excessive_time(recent_activities)
        if excessive_time:
            concerns.append(excessive_time)

        overall_score = max(0.0, 1.0 - sum(c.severity for c in concerns))

        return WellbeingAssessment(
            user_id=user.user_id,
            timestamp=datetime.now(),
            overall_score=overall_score,
            concerns=concerns,
            positive_indicators=[],
            intervention_recommended=any(c.severity > 0.7 for c in concerns)
        )

    def _check_excessive_time(self, recent_activities: List[ActivityEvent]) -> Optional[WellbeingConcern]:
        daily_hours = defaultdict(float)

        # Sort activities to calculate duration between them
        sorted_activities = sorted(recent_activities, key=lambda a: a.timestamp)

        for i in range(1, len(sorted_activities)):
            duration = (sorted_activities[i].timestamp - sorted_activities[i-1].timestamp).total_seconds() / 3600
            # Cap duration at a reasonable value to avoid counting long breaks
            if duration < self.max_daily_hours:
                daily_hours[sorted_activities[i].timestamp.date()] += duration

        excessive_days = {day: hours for day, hours in daily_hours.items() if hours > self.max_daily_hours}

        if excessive_days:
            avg_excessive_hours = np.mean(list(excessive_days.values()))
            severity = min((avg_excessive_hours - self.max_daily_hours) / self.max_daily_hours, 1.0)

            return WellbeingConcern(
                concern_type="excessive_time",
                severity=severity,
                description=f"Spending {avg_excessive_hours:.1f} hours/day",
                detected_at=datetime.now(),
                recommendations=["Set daily time limits"]
            )

        return None
