from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SyntheticProfile:
    name: str
    subject: str
    target: str
    target_skill: float
    prerequisite: str | None = None
    prerequisite_skill: float | None = None
    error_code: str | None = None
    support_dependence: float = 0.0
    volatility: float = 0.08
    transfer_skill: float | None = None
    learning_gain: float = 0.04
    prerequisite_gain: float = 0.12
    profile_kind: str = "typical"


PROFILES = (
    SyntheticProfile("strong_math", "mathematics", "math.numbers.percentages", 0.93, transfer_skill=0.90, volatility=0.03, profile_kind="strong"),
    SyntheticProfile("typical_math", "mathematics", "math.numbers.proportions", 0.76, transfer_skill=0.68, volatility=0.06),
    SyntheticProfile("prerequisite_gap_math", "mathematics", "math.numbers.proportions", 0.42, "math.numbers.ratios", 0.35, "missing_prerequisite", 0.10, 0.05, 0.45, 0.04, 0.16, "prerequisite_gap"),
    SyntheticProfile("support_dependent_math", "mathematics", "math.relations.first-degree-equations", 0.80, transfer_skill=0.65, support_dependence=0.78, volatility=0.05, profile_kind="support_dependent"),
    SyntheticProfile("intermittent_math", "mathematics", "math.numbers.signed-operations", 0.72, transfer_skill=0.60, volatility=0.22, profile_kind="intermittent"),
    SyntheticProfile("conceptual_math", "mathematics", "math.geometry.volume", 0.48, error_code="conceptual_error", transfer_skill=0.40, volatility=0.05, profile_kind="conceptual_gap"),
    SyntheticProfile("strong_english", "english", "eng.reading.a2_everyday_texts", 0.92, transfer_skill=0.88, volatility=0.04, profile_kind="strong"),
    SyntheticProfile("typical_english", "english", "eng.grammar.present_perfect_vs_past", 0.77, transfer_skill=0.70, volatility=0.07),
    SyntheticProfile("prerequisite_gap_english", "english", "eng.grammar.present_perfect_experience", 0.44, "eng.grammar.past_irregular", 0.38, "missing_prerequisite", 0.08, 0.05, 0.48, 0.04, 0.15, "prerequisite_gap"),
    SyntheticProfile("support_dependent_english", "english", "eng.production.experience_future_opinion", 0.82, transfer_skill=0.68, support_dependence=0.80, volatility=0.06, profile_kind="support_dependent"),
    SyntheticProfile("intermittent_english", "english", "eng.listening.a2_conversations", 0.73, transfer_skill=0.62, volatility=0.20, profile_kind="intermittent"),
    SyntheticProfile("strategy_english", "english", "eng.reading.a2_exam_strategies", 0.55, error_code="strategy_selection", transfer_skill=0.45, volatility=0.07, profile_kind="strategy_gap"),
)
