
import unittest
from lsp_core.models import (
    InternalProfile,
    SocialProfile,
    UserPreferences,
    ActivityDomain,
    CapabilityDimension
)
from datetime import datetime

class TestModels(unittest.TestCase):

    def test_internal_profile_creation(self):
        """Test that an InternalProfile can be created with default and specific values."""
        profile = InternalProfile(user_id="user123")
        self.assertEqual(profile.user_id, "user123")
        self.assertEqual(profile.activity_history, [])
        self.assertEqual(profile.capability_scores, {})
        self.assertEqual(profile.learning_curves, {})
        self.assertEqual(profile.behavior_patterns, {})
        self.assertIsNone(profile.preferences)
        self.assertIsNone(profile.engagement_rhythms)
        self.assertEqual(profile.external_connections, {})

        prefs = UserPreferences(display_name="Jules")
        profile_with_prefs = InternalProfile(user_id="user456", preferences=prefs)
        self.assertEqual(profile_with_prefs.user_id, "user456")
        self.assertEqual(profile_with_prefs.preferences.display_name, "Jules")


    def test_social_profile_creation(self):
        """Test that a SocialProfile can be created with default values."""
        profile = SocialProfile(user_id="user123", display_name="Jules")
        self.assertEqual(profile.user_id, "user123")
        self.assertEqual(profile.display_name, "Jules")
        self.assertEqual(profile.badges, [])
        self.assertEqual(profile.ranks, {})
        self.assertEqual(profile.public_scores, {})
        self.assertEqual(profile.social_capital, 0.0)
        self.assertEqual(profile.reputation_score, 0.0)
        self.assertEqual(profile.rated_contributions, [])
        self.assertEqual(profile.achievement_timeline, [])
        self.assertEqual(profile.peer_ratings, [])

    def test_user_preferences_creation(self):
        """Test that UserPreferences can be created."""
        prefs_empty = UserPreferences()
        self.assertIsNone(prefs_empty.display_name)

        prefs_with_name = UserPreferences(display_name="Jules")
        self.assertEqual(prefs_with_name.display_name, "Jules")


if __name__ == '__main__':
    unittest.main()
