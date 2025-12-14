
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
    RewardConcept
)
from lsp_core.algorithm import (
    MultiDimensionalAssessor,
    PatternDiscoveryEngine,
    RewardSynthesizer,
    EligibilityDeterminer
)

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

        updated_scores = self.assessor.assess_from_activity(event, self.profile)

        self.assertGreater(updated_scores[CapabilityDimension.DOMAIN_DEPTH], 0.5)
        self.assertGreater(updated_scores[CapabilityDimension.RELIABILITY], 0.5)
        self.assertNotIn(CapabilityDimension.LEARNING_SPEED, updated_scores)

class TestPatternDiscoveryEngine(unittest.TestCase):

    def setUp(self):
        self.engine = PatternDiscoveryEngine()
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

        self.assertIsNotNone(patterns)
        self.assertGreater(len(patterns), 0)

        creative_pattern_found = any(p.capability_profile[CapabilityDimension.CREATIVITY] > 0.7 for p in patterns)
        analytical_pattern_found = any(p.capability_profile[CapabilityDimension.ANALYTICAL_THINKING] > 0.7 for p in patterns)

        self.assertTrue(creative_pattern_found, "A creative-dominant pattern was not found.")
        self.assertTrue(analytical_pattern_found, "An analytical-dominant pattern was not found.")

class TestRewardSynthesizer(unittest.TestCase):
    def setUp(self):
        self.synthesizer = RewardSynthesizer()
        self.user_population = [] # Not used in this test

    def test_synthesize_sdt_rewards(self):
        """Test that SDT-based rewards are synthesized for relevant patterns."""
        patterns = [
            BehaviorPattern(pattern_id="p1", pattern_name="Adaptable Learners", description="", characteristic_behaviors=[], capability_profile={CapabilityDimension.ADAPTABILITY: 0.8}, temporal_signature={}, strength=1, consistency=1, triggering_contexts=[]),
            BehaviorPattern(pattern_id="p2", pattern_name="Persistent Achievers", description="", characteristic_behaviors=[], capability_profile={CapabilityDimension.PERSISTENCE: 0.9}, temporal_signature={}, strength=1, consistency=1, triggering_contexts=[]),
            BehaviorPattern(pattern_id="p3", pattern_name="Team Players", description="", characteristic_behaviors=[], capability_profile={CapabilityDimension.COLLABORATION: 0.8}, temporal_signature={}, strength=1, consistency=1, triggering_contexts=[]),
            BehaviorPattern(pattern_id="p4", pattern_name="Neutral Profile", description="", characteristic_behaviors=[], capability_profile={CapabilityDimension.KNOWLEDGE_BREADTH: 0.6}, temporal_signature={}, strength=1, consistency=1, triggering_contexts=[]),
        ]

        new_rewards = self.synthesizer.synthesize_new_rewards(patterns, self.user_population)

        self.assertEqual(len(new_rewards), 3)
        reward_names = {r.concept_name for r in new_rewards}
        self.assertIn("Self-Directed Learner", reward_names)
        self.assertIn("Perseverance Award", reward_names)
        self.assertIn("Valued Collaborator", reward_names)

class TestEligibilityDeterminer(unittest.TestCase):
    def setUp(self):
        self.determiner = EligibilityDeterminer()
        self.user_eligible = InternalProfile(user_id="eligible_user", capability_scores={CapabilityDimension.PERSISTENCE: 0.9})
        self.user_ineligible = InternalProfile(user_id="ineligible_user", capability_scores={CapabilityDimension.PERSISTENCE: 0.5})

        target_pattern = BehaviorPattern(pattern_id="p_persist", pattern_name="Persistent Achievers", description="", characteristic_behaviors=[], capability_profile={CapabilityDimension.PERSISTENCE: 0.85}, temporal_signature={}, strength=1, consistency=1, triggering_contexts=[])

        self.reward_concept = RewardConcept(
            concept_id="competence_p_persist",
            concept_name="Perseverance Award",
            concept_type="recognition",
            target_pattern=target_pattern,
            value_to_users=0.85,
            eligibility_model=None,
            delivery_mechanism="timeline_highlight",
            social_visibility="public",
            iterations=1,
            user_feedback_score=0.0
        )

    def test_determine_eligibility(self):
        """Test that eligibility is determined correctly based on user capabilities."""
        is_eligible = self.determiner.determine_eligibility(self.user_eligible, self.reward_concept)
        is_ineligible = self.determiner.determine_eligibility(self.user_ineligible, self.reward_concept)

        self.assertTrue(is_eligible)
        self.assertFalse(is_ineligible)

if __name__ == '__main__':
    unittest.main()
