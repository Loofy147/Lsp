
import unittest
from lsp_core.models import BehaviorPattern, RewardConcept, CapabilityDimension
from lsp_core.rewards import RewardSynthesizer

class TestRewardSynthesizer(unittest.TestCase):

    def setUp(self):
        self.synthesizer = RewardSynthesizer()

    def test_synthesize_competence_reward(self):
        pattern = BehaviorPattern(
            pattern_id="p1",
            pattern_name="Consistent High Performer",
            description="User consistently performs well in creative tasks.",
            capability_profile={CapabilityDimension.CREATIVITY: 0.8},
            triggering_contexts=[],
            characteristic_behaviors=[],
            temporal_signature={},
            strength=0.9,
            consistency=0.9,
        )
        reward = self.synthesizer.synthesize_reward_concept(pattern)
        self.assertEqual(reward.concept_type, "skill_badge")
        self.assertIn("Mastery", reward.concept_name)

    def test_synthesize_autonomy_reward(self):
        pattern = BehaviorPattern(
            pattern_id="p2",
            pattern_name="Explorer",
            description="User explores diverse activities.",
            capability_profile={},
            triggering_contexts=["a", "b", "c", "d"],
            characteristic_behaviors=[],
            temporal_signature={},
            strength=0.7,
            consistency=0.8,
        )
        reward = self.synthesizer.synthesize_reward_concept(pattern)
        self.assertEqual(reward.concept_type, "choice_opportunity")
        self.assertIn("Explorer", reward.concept_name)

    def test_synthesize_relatedness_reward(self):
        pattern = BehaviorPattern(
            pattern_id="p3",
            pattern_name="Collaborator",
            description="User frequently collaborates with others.",
            capability_profile={},
            triggering_contexts=[],
            characteristic_behaviors=[],
            temporal_signature={},
            strength=0.8,
            consistency=0.8,
        )
        reward = self.synthesizer.synthesize_reward_concept(pattern)
        self.assertEqual(reward.concept_type, "social_recognition")
        self.assertIn("Community Contributor", reward.concept_name)

if __name__ == '__main__':
    unittest.main()
