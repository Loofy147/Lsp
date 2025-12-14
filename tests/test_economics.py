
import unittest
from lsp_core.models import EconomicScenario, EconomicProjection
from lsp_core.economics import EconomicModeler

class TestEconomics(unittest.TestCase):

    def test_economic_modeler(self):
        """Test the EconomicModeler with a simple scenario."""
        modeler = EconomicModeler(fixed_costs_monthly=10000, platform_revenue_share=0.3)
        scenario = EconomicScenario(
            name="Test Scenario",
            num_users=1000,
            monthly_active_users=500,
            ad_cpm=2.0,
            ad_views_per_active_user_monthly=100,
            ad_opt_out_rate=0.1,
            avg_monthly_freelance_transactions=50,
            avg_transaction_value=100,
            platform_commission_rate=0.1,
            premium_subscription_rate=0.1,
            premium_monthly_price=10,
            business_subscribers=5,
            business_subscription_monthly=100,
            credential_verifications_monthly=20,
            verification_fee=25
        )

        projection = modeler.project_economics(scenario)
        self.assertIsInstance(projection, EconomicProjection)
        self.assertGreater(projection.total_revenue_monthly, 0)
        self.assertEqual(projection.platform_share, projection.total_revenue_monthly * 0.3)
        self.assertTrue(projection.is_viable in [True, False])

if __name__ == '__main__':
    unittest.main()
