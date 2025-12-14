
"""
LSP Social Profile Manager
- Manages the translation of internal achievements to the public SocialProfile.
- Handles reputation, badges, and other social mechanics.
"""

from .models import InternalProfile, SocialProfile, BehaviorPattern, Badge, Achievement
from datetime import datetime

class SocialProfileUpdater:
    """
    Updates a user's SocialProfile based on their InternalProfile.
    This acts as a bridge, ensuring the social representation is a curated
    reflection of genuine, validated growth.
    """

    def update_profile(self, internal_profile: InternalProfile, social_profile: SocialProfile) -> SocialProfile:
        """
        The main entry point to update a social profile from its internal counterpart.
        """
        social_profile = self._award_badges_for_patterns(internal_profile, social_profile)
        # Future methods for updating rank, reputation, etc., will be called here.

        return social_profile

    def _award_badges_for_patterns(self, internal_profile: InternalProfile, social_profile: SocialProfile) -> SocialProfile:
        """
        Awards badges for newly validated, high-strength behavior patterns.
        """
        existing_badge_patterns = {badge.badge_id for badge in social_profile.badges}

        for pattern_id, pattern in internal_profile.behavior_patterns.items():
            # Define criteria for a pattern to be badge-worthy
            is_badge_worthy = pattern.strength > 0.8 and pattern.consistency > 0.8

            # Check if a badge for this pattern has already been awarded
            badge_id = f"badge_{pattern_id}"
            if is_badge_worthy and badge_id not in existing_badge_patterns:

                # Create a new badge
                new_badge = Badge(
                    badge_id=badge_id,
                    name=f"Exemplar: {pattern.pattern_name}",
                    description=f"Demonstrated a strong and consistent pattern of '{pattern.description}'.",
                    icon_data="<svg>...</svg>", # Placeholder for icon
                    rarity=1.0 - pattern.strength, # Rarer for stronger patterns
                    prestige_score=pattern.strength * 100
                )

                # Create a corresponding achievement timeline event
                new_achievement = Achievement(
                    achievement_id=f"ach_{badge_id}",
                    user_id=internal_profile.user_id,
                    timestamp=datetime.now(),
                    reward_concept_id=new_badge.badge_id, # Link to the badge
                    specific_instance={"pattern_strength": pattern.strength, "consistency": pattern.consistency},
                    earning_journey=[f"Validated pattern '{pattern.pattern_name}'"]
                )

                social_profile.badges.append(new_badge)
                social_profile.achievement_timeline.append(new_achievement)

        return social_profile
