
import unittest
from datetime import datetime
from lsp_core.models import (
    InternalProfile,
    ActivityEvent,
    ActivityContext,
    ActivityDomain,
    CapabilityDimension,
    LearningCurve
)
from lsp_core.algorithm import MultiDimensionalAssessor, PatternDiscoveryEngine

class TestMultiDimensionalAssessor(unittest.TestCase):

    def setUp(self):
        self.assessor = MultiDimensionalAssessor()
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

        updated_scores = self.assessor.assess_from_activity(event, self.profile)

        # Check that PATTERN_RECOGNITION score has increased significantly
        self.assertGreater(updated_scores[CapabilityDimension.PATTERN_RECOGNITION], 0.5)
        # Check that ANALYTICAL_THINKING score has also increased
        self.assertGreater(updated_scores[CapabilityDimension.ANALYTICAL_THINKING], 0.5)
        # Check that a non-related score (e.g., CREATIVITY) is not updated
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

        updated_scores = self.assessor.assess_from_activity(event, self.profile)

        # Check that DOMAIN_DEPTH and RELIABILITY scores have increased
        self.assertGreater(updated_scores[CapabilityDimension.DOMAIN_DEPTH], 0.5)
        self.assertGreater(updated_scores[CapabilityDimension.RELIABILITY], 0.5)
        # Check that a non-related score is not updated
        self.assertNotIn(CapabilityDimension.LEARNING_SPEED, updated_scores)

class TestPatternDiscoveryEngine(unittest.TestCase):

    def setUp(self):
        self.engine = PatternDiscoveryEngine()
        # Create a population of users with distinct profiles
        self.user_population = [
            InternalProfile(user_id="user1", capability_scores={CapabilityDimension.CREATIVITY: 0.8, CapabilityDimension.ANALYTICAL_THINKING: 0.3}),
            InternalProfile(user_id="user2", capability_scores={CapabilityDimension.CREATIVITY: 0.85, CapabilityDimension.ANALYTICAL_THINKING: 0.25}),
            InternalProfile(user_id="user3", capability_scores={CapabilityDimension.CREATIVITY: 0.3, CapabilityDimension.ANALYTICAL_THINKING: 0.9}),
            InternalProfile(user_id="user4", capability_scores={CapabilityDimension.CREATIVITY: 0.25, CapabilityDimension.ANALYTICAL_THINKING: 0.95}),
            InternalProfile(user_id="user5", capability_scores={CapabilityDimension.LEARNING_SPEED: 0.9, CapabilityDimension.PERSISTENCE: 0.8}),
            InternalProfile(user_id="user6", capability_scores={CapabilityDimension.LEARNING_SPEED: 0.95, CapabilityDimension.PERSISTENCE: 0.85}),
        ]

    def test_discover_patterns(self):
        """Test that the engine discovers meaningful patterns in a user population."""
        patterns = self.engine.discover_patterns(self.user_population)

        # Check that patterns are discovered
        self.assertIsNotNone(patterns)
        self.assertGreater(len(patterns), 0)

        # Check that the discovered patterns have distinct capability profiles
        creative_pattern_found = False
        analytical_pattern_found = False

        for p in patterns:
            if p.capability_profile[CapabilityDimension.CREATIVITY] > 0.7:
                creative_pattern_found = True
            if p.capability_profile[CapabilityDimension.ANALYTICAL_THINKING] > 0.7:
                analytical_pattern_found = True

        self.assertTrue(creative_pattern_found, "A creative-dominant pattern was not found.")
        self.assertTrue(analytical_pattern_found, "An analytical-dominant pattern was not found.")


if __name__ == '__main__':
    unittest.main()
