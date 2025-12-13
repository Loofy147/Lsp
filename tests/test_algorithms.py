
import unittest
from datetime import datetime, timedelta
from lsp_core.models import (
    ActivityEvent,
    InternalProfile,
    CapabilityDimension,
    LanguageCapabilityDimension,
    LanguageAssessmentActivity,
    CapabilityEstimate,
    UserPreferences,
    ActivityContext,
    ActivityDomain,
)
from lsp_core.algorithm import (
    FraudDetector,
    LanguageCapabilityAssessor,
    PatternValidator,
    WellbeingMonitor,
    PatternDiscoveryEngine,
)

class TestAlgorithms(unittest.TestCase):

    def setUp(self):
        """Set up common test data."""
        self.user = InternalProfile(
            user_id="test_user",
            preferences=UserPreferences(display_name="Test"),
            capability_scores={
                CapabilityDimension.CREATIVITY: CapabilityEstimate(mean=0.8, variance=0.1, confidence=0.9)
            }
        )
        self.user.activity_history = [
            ActivityEvent(
                event_id=f"event_{i}",
                user_id="test_user",
                timestamp=datetime.now() - timedelta(days=i),
                domain=ActivityDomain.CREATIVE_WORK,
                activity_type="writing",
                action_data={},
                context=ActivityContext(time_of_day="morning", day_of_week="monday", device_type="desktop", location_type="home"),
                performance_metrics={},
                capability_signals={},
                session_id="session1",
                sequence_position=i,
                engagement_level=0.8
            ) for i in range(10)
        ]

    def test_wellbeing_monitor(self):
        """Test the WellbeingMonitor for detecting excessive use."""
        monitor = WellbeingMonitor()

        # Simulate a burst of activity within a few hours
        now = datetime.now()
        for i in range(20): # 20 events, 15 minutes apart = 5 hours
            self.user.activity_history.append(ActivityEvent(
                event_id=f"event_burst_{i}", user_id="test_user",
                timestamp=now - timedelta(minutes=15 * (20-i)),
                domain=ActivityDomain.CREATIVE_WORK, activity_type="writing", action_data={},
                context=ActivityContext(time_of_day="night", day_of_week="tuesday", device_type="desktop", location_type="home"),
                performance_metrics={}, capability_signals={}, session_id="session3",
                sequence_position=i, engagement_level=0.9
            ))

        assessment = monitor.assess_wellbeing(self.user)
        self.assertTrue(any(c.concern_type == "excessive_time" for c in assessment.concerns))

    def test_pattern_discovery(self):
        """Test that the PatternDiscoveryEngine can generate patterns."""
        engine = PatternDiscoveryEngine(n_clusters=1)
        users = [self.user]
        patterns = engine.discover_patterns(users)
        self.assertEqual(len(patterns), 1)
        self.assertIn("strong in creativity", patterns[0].description)

if __name__ == '__main__':
    unittest.main()
