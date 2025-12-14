import unittest
from lsp_core.models import (
    InternalProfile,
    BehaviorPattern,
    CapabilityDimension,
    RewardConcept,
    CapabilityEstimate
)
from lsp_core.rewards import (
    RewardSynthesizer,
    EligibilityDeterminer
)

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

        new_rewards = [self.synthesizer.synthesize_reward_concept(p) for p in patterns]

        self.assertEqual(len(new_rewards), 4)
        reward_names = {r.concept_name for r in new_rewards}
        self.assertIn("Mastery of Adaptable Learners", reward_names)
        self.assertIn("Mastery of Persistent Achievers", reward_names)
        self.assertIn("Mastery of Team Players", reward_names)

class TestEligibilityDeterminer(unittest.TestCase):
    def setUp(self):
        self.determiner = EligibilityDeterminer()
        self.user_eligible = InternalProfile(user_id="eligible_user", capability_scores={CapabilityDimension.PERSISTENCE: CapabilityEstimate(mean=0.9, variance=0.1, confidence=0.8)})
        self.user_ineligible = InternalProfile(user_id="ineligible_user", capability_scores={CapabilityDimension.PERSISTENCE: CapabilityEstimate(mean=0.5, variance=0.1, confidence=0.8)})

        self.test_pattern = BehaviorPattern(
            pattern_id="p_persist",
            pattern_name="Persistent Achievers",
            description="Users who demonstrate high levels of persistence.",
            capability_profile={CapabilityDimension.PERSISTENCE: 0.85},
            characteristic_behaviors=[],
            temporal_signature={},
            strength=0.9,
            consistency=0.9,
            triggering_contexts=[]
        )

    def test_determine_eligibility(self):
        """Test that eligibility is determined correctly based on user capabilities."""
        is_eligible = self.determiner.is_eligible_for_pattern(self.user_eligible, self.test_pattern)
        is_ineligible = self.determiner.is_eligible_for_pattern(self.user_ineligible, self.test_pattern)

        self.assertTrue(is_eligible)
        self.assertFalse(is_ineligible)

if __name__ == '__main__':
    unittest.main()
