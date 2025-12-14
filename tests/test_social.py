
import unittest
from lsp_core.models import InternalProfile, SocialProfile, BehaviorPattern, Badge, Achievement
from lsp_core.social import SocialProfileUpdater

class TestSocialProfileUpdater(unittest.TestCase):

    def setUp(self):
        self.updater = SocialProfileUpdater()
        self.internal_profile = InternalProfile(user_id="user1")
        self.social_profile = SocialProfile(user_id="user1", display_name="User One")

    def test_award_badge_for_strong_pattern(self):
        pattern = BehaviorPattern(
            pattern_id="p1",
            pattern_name="Creative Genius",
            description="Consistently high creativity.",
            strength=0.9,
            consistency=0.9,
            characteristic_behaviors=[],
            capability_profile={},
            temporal_signature={},
            triggering_contexts=[]
        )
        self.internal_profile.behavior_patterns["p1"] = pattern

        updated_profile = self.updater.update_profile(self.internal_profile, self.social_profile)

        self.assertEqual(len(updated_profile.badges), 1)
        self.assertEqual(updated_profile.badges[0].name, "Exemplar: Creative Genius")
        self.assertEqual(len(updated_profile.achievement_timeline), 1)
        self.assertEqual(updated_profile.achievement_timeline[0].reward_concept_id, "badge_p1")

    def test_no_badge_for_weak_pattern(self):
        pattern = BehaviorPattern(
            pattern_id="p2",
            pattern_name="Dabbler",
            description="Tries a little of everything.",
            strength=0.5,
            consistency=0.5,
            characteristic_behaviors=[],
            capability_profile={},
            temporal_signature={},
            triggering_contexts=[]
        )
        self.internal_profile.behavior_patterns["p2"] = pattern

        updated_profile = self.updater.update_profile(self.internal_profile, self.social_profile)

        self.assertEqual(len(updated_profile.badges), 0)

if __name__ == '__main__':
    unittest.main()
