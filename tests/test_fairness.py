
import unittest
from lsp_core.models import (
    InternalProfile,
    Achievement,
    FairnessConfig,
    FairnessMetric,
    FairnessAuditReport,
)
from lsp_core.fairness import FairnessAuditor
from datetime import datetime

class TestFairness(unittest.TestCase):

    def test_fairness_auditor(self):
        """Test the FairnessAuditor for bias detection."""
        config = FairnessConfig(
            primary_metric=FairnessMetric.STATISTICAL_PARITY,
            protected_attributes=["location"],
            acceptable_disparity_threshold=0.1
        )
        auditor = FairnessAuditor(config)

        users = [
            InternalProfile(user_id=f"user_{i}") for i in range(10)
        ]
        rewards = {f"user_{i}": [Achievement(achievement_id=f"ach_{i}", user_id=f"user_{i}", timestamp=datetime.now(), reward_concept_id="test", specific_instance={}, earning_journey=[])] for i in range(5)}
        demographics = {
            f"user_{i}": {"location": "A"} for i in range(5)
        }
        demographics.update({
            f"user_{i}": {"location": "B"} for i in range(5, 10)
        })

        reports = auditor.audit_reward_distribution(users, rewards, demographics)
        self.assertEqual(len(reports), 1)
        report = reports[0]
        self.assertIsInstance(report, FairnessAuditReport)
        self.assertFalse(report.passes_threshold) # Group A has 100% rewards, Group B has 0%
        self.assertGreater(report.max_disparity, 0.9)

if __name__ == '__main__':
    unittest.main()
