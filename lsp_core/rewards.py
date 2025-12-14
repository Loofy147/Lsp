
"""
LSP Reward Synthesizer
- Generates meaningful reward concepts from validated behavior patterns.
- Based on Self-Determination Theory (SDT) to foster intrinsic motivation.
"""

from .models import BehaviorPattern, RewardConcept, CapabilityDimension
import random

class RewardSynthesizer:
    """
    Designs RewardConcepts that align with user autonomy, competence, and relatedness.
    """

    def synthesize_reward_concept(self, pattern: BehaviorPattern) -> RewardConcept:
        """
        Takes a validated behavior pattern and generates a tailored RewardConcept.
        """
        # Step 1: Analyze the pattern to understand its core motivational driver.
        dominant_driver = self._analyze_pattern(pattern)

        # Step 2: Select a reward strategy based on the driver.
        if dominant_driver == "competence":
            return self._create_competence_reward(pattern)
        elif dominant_driver == "autonomy":
            return self._create_autonomy_reward(pattern)
        else: # "relatedness" or fallback
            return self._create_relatedness_reward(pattern)

    def _analyze_pattern(self, pattern: BehaviorPattern) -> str:
        """
        Analyzes a pattern to determine the primary SDT driver.
        This is a simplified analysis. A production system would be more complex.
        """
        # High capability scores suggest a competence driver.
        if any(score > 0.7 for score in pattern.capability_profile.values()):
            return "competence"

        # Patterns triggered by diverse, user-initiated contexts suggest autonomy.
        if len(pattern.triggering_contexts) > 3:
            return "autonomy"

        # Patterns involving collaboration or social activities point to relatedness.
        if "collaborat" in pattern.description.lower() or \
           "social" in pattern.pattern_name.lower() or \
           "collaborat" in pattern.pattern_name.lower():
            return "relatedness"

        # Fallback heuristic
        return random.choice(["competence", "autonomy", "relatedness"])

    def _create_competence_reward(self, pattern: BehaviorPattern) -> RewardConcept:
        """
        Creates a reward that acknowledges skill and mastery.
        """
        return RewardConcept(
            concept_id=f"rc_{pattern.pattern_id}_competence",
            concept_name=f"Mastery of {pattern.pattern_name}",
            concept_type="skill_badge",
            target_pattern_id=pattern.pattern_id,
            value_to_users=0.8,
            eligibility_criteria={"min_pattern_strength": 0.75},
            delivery_mechanism="badge_award",
            social_visibility="public_optional",
            iterations=1,
            user_feedback_score=0.0
        )

    def _create_autonomy_reward(self, pattern: BehaviorPattern) -> RewardConcept:
        """
        Creates a reward that offers choice and freedom.
        """
        return RewardConcept(
            concept_id=f"rc_{pattern.pattern_id}_autonomy",
            concept_name=f"Creative Explorer: {pattern.pattern_name}",
            concept_type="choice_opportunity",
            target_pattern_id=pattern.pattern_id,
            value_to_users=0.7,
            eligibility_criteria={"min_consistency": 0.7},
            delivery_mechanism="unlock_feature",
            social_visibility="private",
            iterations=1,
            user_feedback_score=0.0
        )

    def _create_relatedness_reward(self, pattern: BehaviorPattern) -> RewardConcept:
        """
        Creates a reward that fosters social connection.
        """
        return RewardConcept(
            concept_id=f"rc_{pattern.pattern_id}_relatedness",
            concept_name=f"Community Contributor: {pattern.pattern_name}",
            concept_type="social_recognition",
            target_pattern_id=pattern.pattern_id,
            value_to_users=0.75,
            eligibility_criteria={"min_engagement": 0.6},
            delivery_mechanism="shoutout_on_feed",
            social_visibility="public",
            iterations=1,
            user_feedback_score=0.0
        )
