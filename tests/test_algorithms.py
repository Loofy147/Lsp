
import unittest
from datetime import datetime
from lsp_core.models import (
    InternalProfile,
    ActivityEvent,
    ActivityContext,
    ActivityDomain,
    CapabilityDimension,
    BehaviorPattern,
    LearningCurve,
    RewardConcept,
    CapabilityEstimate
)
from lsp_core.algorithm import (
    MultiDimensionalAssessor,
    PatternDiscoveryEngine
)

class TestMultiDimensionalAssessor(unittest.TestCase):

    def setUp(self):
        self.assessor = MultiDimensionalAssessor(dimensions=list(CapabilityDimension))
        self.profile = InternalProfile(user_id="test_user")

    def test_assessment_from_skill_game(self):
        """Test that a skill game activity updates the correct capabilities."""
        event = ActivityEvent(
            event_id="evt1", user_id="test_user", timestamp=datetime.now(),
            domain=ActivityDomain.SKILL_GAMES, activity_type="puzzle",
            action_data={}, context=ActivityContext(time_of_day="evening", day_of_week="saturday", device_type="mobile", location_type="home", previous_activities=[], time_since_last_activity=0, current_goals=[], active_learning_paths=[], recent_achievements=[], collaborative=False, influenced_by_peers=False),
            performance_metrics={'score': 80, 'strategy_score': 0.9},
            capability_signals={}, session_id="sess1", sequence_position=1,
            engagement_level=0.9, frustration_indicators=[], flow_state_indicators=["focus"]
        )

        updated_scores = self.assessor.assess_from_activity(
            activity=event,
            performance_signals=event.performance_metrics,
            dimensions_assessed=[CapabilityDimension.PATTERN_RECOGNITION, CapabilityDimension.ANALYTICAL_THINKING]
        )

        self.assertGreater(updated_scores[CapabilityDimension.PATTERN_RECOGNITION], 0.5)
        self.assertGreater(updated_scores[CapabilityDimension.ANALYTICAL_THINKING], 0.5)
        self.assertNotIn(CapabilityDimension.CREATIVITY, updated_scores)

    def test_assessment_from_freelance_project(self):
        """Test that a freelance project activity updates the correct capabilities."""
        event = ActivityEvent(
            event_id="evt2", user_id="test_user", timestamp=datetime.now(),
            domain=ActivityDomain.FREELANCE_PROJECTS, activity_type="translation",
            action_data={}, context=ActivityContext(time_of_day="morning", day_of_week="monday", device_type="desktop", location_type="work", previous_activities=[], time_since_last_activity=0, current_goals=[], active_learning_paths=[], recent_achievements=[], collaborative=False, influenced_by_peers=False),
            performance_metrics={'quality_rating': 4.5, 'on_time_delivery': 1.0},
            capability_signals={}, session_id="sess2", sequence_position=1,
            engagement_level=0.8, frustration_indicators=[], flow_state_indicators=[]
        )

        updated_scores = self.assessor.assess_from_activity(
            activity=event,
            performance_signals=event.performance_metrics,
            dimensions_assessed=[CapabilityDimension.DOMAIN_DEPTH, CapabilityDimension.RELIABILITY]
        )

        self.assertGreater(updated_scores[CapabilityDimension.DOMAIN_DEPTH], 0.5)
        self.assertGreater(updated_scores[CapabilityDimension.RELIABILITY], 0.5)
        self.assertNotIn(CapabilityDimension.LEARNING_SPEED, updated_scores)

class TestPatternDiscoveryEngine(unittest.TestCase):

    def setUp(self):
        self.engine = PatternDiscoveryEngine()
        self.user_population = [
            InternalProfile(user_id="user1", capability_scores={CapabilityDimension.CREATIVITY: CapabilityEstimate(mean=0.8, variance=0.1, confidence=0.8), CapabilityDimension.ANALYTICAL_THINKING: CapabilityEstimate(mean=0.3, variance=0.1, confidence=0.8)}),
            InternalProfile(user_id="user2", capability_scores={CapabilityDimension.CREATIVITY: CapabilityEstimate(mean=0.85, variance=0.1, confidence=0.8), CapabilityDimension.ANALYTICAL_THINKING: CapabilityEstimate(mean=0.25, variance=0.1, confidence=0.8)}),
            InternalProfile(user_id="user3", capability_scores={CapabilityDimension.CREATIVITY: CapabilityEstimate(mean=0.3, variance=0.1, confidence=0.8), CapabilityDimension.ANALYTICAL_THINKING: CapabilityEstimate(mean=0.9, variance=0.1, confidence=0.8)}),
            InternalProfile(user_id="user4", capability_scores={CapabilityDimension.CREATIVITY: CapabilityEstimate(mean=0.25, variance=0.1, confidence=0.8), CapabilityDimension.ANALYTICAL_THINKING: CapabilityEstimate(mean=0.95, variance=0.1, confidence=0.8)}),
            InternalProfile(user_id="user5", capability_scores={CapabilityDimension.LEARNING_SPEED: CapabilityEstimate(mean=0.9, variance=0.1, confidence=0.8), CapabilityDimension.PERSISTENCE: CapabilityEstimate(mean=0.8, variance=0.1, confidence=0.8)}),
            InternalProfile(user_id="user6", capability_scores={CapabilityDimension.LEARNING_SPEED: CapabilityEstimate(mean=0.95, variance=0.1, confidence=0.8), CapabilityDimension.PERSISTENCE: CapabilityEstimate(mean=0.85, variance=0.1, confidence=0.8)}),
        ]

    def test_discover_patterns(self):
        """Test that the engine discovers meaningful patterns in a user population."""
        patterns = self.engine.discover_patterns(self.user_population)

        self.assertIsNotNone(patterns)
        self.assertGreater(len(patterns), 0)

        creative_pattern_found = any(p.capability_profile.get(CapabilityDimension.CREATIVITY, 0) > 0.7 for p in patterns)
        analytical_pattern_found = any(p.capability_profile.get(CapabilityDimension.ANALYTICAL_THINKING, 0) > 0.7 for p in patterns)

        self.assertTrue(creative_pattern_found, "A creative-dominant pattern was not found.")
        self.assertTrue(analytical_pattern_found, "An analytical-dominant pattern was not found.")

if __name__ == '__main__':
    unittest.main()
