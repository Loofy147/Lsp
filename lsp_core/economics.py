
"""
LSP Economic Modeling System
- Provides a production-ready economic modeler to validate the platform's financial viability.
- Replaces the original placeholder economic system.
"""

from typing import Dict
from .models import EconomicScenario, EconomicProjection

# ============================================================================
# ECONOMIC MODELING & VALIDATION
# ============================================================================

class EconomicModeler:
    """
    Models platform economics under different scenarios.
    Validates whether the revenue model is sustainable.
    """

    def __init__(
        self,
        fixed_costs_monthly: float = 50000,  # Servers, staff, etc.
        platform_revenue_share: float = 0.4
    ):
        self.fixed_costs_monthly = fixed_costs_monthly
        self.platform_revenue_share = platform_revenue_share

    def project_economics(
        self,
        scenario: EconomicScenario
    ) -> EconomicProjection:
        """
        Project economics for a given scenario.
        Returns a detailed breakdown and viability assessment.
        """
        # 1. Advertising Revenue
        active_ad_viewers = scenario.monthly_active_users * (1 - scenario.ad_opt_out_rate)
        ad_impressions = active_ad_viewers * scenario.ad_views_per_active_user_monthly
        ad_revenue = (ad_impressions / 1000) * scenario.ad_cpm

        # 2. Freelance Commission
        freelance_revenue = (
            scenario.avg_monthly_freelance_transactions *
            scenario.avg_transaction_value *
            scenario.platform_commission_rate
        )

        # 3. Premium Subscriptions
        premium_subscribers = int(scenario.monthly_active_users * scenario.premium_subscription_rate)
        premium_revenue = premium_subscribers * scenario.premium_monthly_price

        # 4. Business Subscriptions
        business_revenue = scenario.business_subscribers * scenario.business_subscription_monthly

        # 5. Credential Verifications
        credential_revenue = scenario.credential_verifications_monthly * scenario.verification_fee

        # Total Revenue
        total_revenue = (
            ad_revenue + freelance_revenue + premium_revenue +
            business_revenue + credential_revenue
        )

        # Distribution
        platform_share = total_revenue * self.platform_revenue_share
        user_pool = total_revenue * (1 - self.platform_revenue_share)

        avg_per_user = user_pool / scenario.monthly_active_users if scenario.monthly_active_users > 0 else 0
        median_per_user = avg_per_user * 0.4  # Simplified Pareto distribution

        # Viability Assessment
        monthly_profit = platform_share - self.fixed_costs_monthly
        is_viable = avg_per_user >= 10.0 and monthly_profit >= 0

        months_to_profitability = 999
        if monthly_profit < 0:
            current_revenue = total_revenue
            for month in range(1, 37):
                current_revenue *= 1.20  # 20% growth
                current_profit = (current_revenue * self.platform_revenue_share) - self.fixed_costs_monthly
                if current_profit >= 0:
                    months_to_profitability = month
                    break
        else:
            months_to_profitability = 0

        runway_months = (1_000_000 / abs(monthly_profit)) if monthly_profit < 0 else 999

        return EconomicProjection(
            scenario_name=scenario.name,
            ad_revenue_monthly=ad_revenue,
            freelance_commission_monthly=freelance_revenue,
            premium_subscription_revenue=premium_revenue,
            business_subscription_revenue=business_revenue,
            credential_revenue_monthly=credential_revenue,
            total_revenue_monthly=total_revenue,
            platform_share=platform_share,
            user_pool=user_pool,
            avg_per_user_monthly=avg_per_user,
            median_per_user_monthly=median_per_user,
            is_viable=is_viable,
            months_to_profitability=months_to_profitability,
            runway_months=runway_months
        )

    def run_scenario_analysis(self) -> Dict[str, EconomicProjection]:
        """
        Run multiple scenarios: best case, expected, worst case.
        """
        scenarios = {
            'worst_case': EconomicScenario(
                name="Worst Case", num_users=1_000, monthly_active_users=300, ad_cpm=1.0,
                ad_views_per_active_user_monthly=50, ad_opt_out_rate=0.6, avg_monthly_freelance_transactions=20,
                avg_transaction_value=100, platform_commission_rate=0.15, premium_subscription_rate=0.02,
                premium_monthly_price=10, business_subscribers=2, business_subscription_monthly=200,
                credential_verifications_monthly=10, verification_fee=25
            ),
            'expected_case': EconomicScenario(
                name="Expected Case", num_users=10_000, monthly_active_users=3_500, ad_cpm=3.0,
                ad_views_per_active_user_monthly=100, ad_opt_out_rate=0.4, avg_monthly_freelance_transactions=300,
                avg_transaction_value=150, platform_commission_rate=0.15, premium_subscription_rate=0.05,
                premium_monthly_price=15, business_subscribers=25, business_subscription_monthly=500,
                credential_verifications_monthly=100, verification_fee=30
            ),
            'best_case': EconomicScenario(
                name="Best Case", num_users=100_000, monthly_active_users=40_000, ad_cpm=8.0,
                ad_views_per_active_user_monthly=150, ad_opt_out_rate=0.3, avg_monthly_freelance_transactions=5000,
                avg_transaction_value=200, platform_commission_rate=0.15, premium_subscription_rate=0.08,
                premium_monthly_price=20, business_subscribers=300, business_subscription_monthly=1000,
                credential_verifications_monthly=1500, verification_fee=35
            )
        }

        return {name: self.project_economics(scenario) for name, scenario in scenarios.items()}

    def print_scenario_analysis(self):
        """Pretty print scenario analysis results"""
        projections = self.run_scenario_analysis()

        print("\\n" + "="*80)
        print("ECONOMIC SCENARIO ANALYSIS")
        print("="*80)

        for proj in projections.values():
            print(f"\\n{proj.scenario_name.upper()}")
            print("-" * 80)
            print(f"  TOTAL REVENUE: ${proj.total_revenue_monthly:12,.2f}")
            print(f"  Platform Share: ${proj.platform_share:12,.2f}")
            print(f"  User Pool:      ${proj.user_pool:12,.2f}")
            print(f"  Avg per user:   ${proj.avg_per_user_monthly:12,.2f}/month")
            print(f"  Is Viable:      {proj.is_viable}")
            print(f"  Months to Profit: {proj.months_to_profitability}")
            print()
