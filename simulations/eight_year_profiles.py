from __future__ import annotations

from dataclasses import dataclass


MATH_SCIENTIFIC_PATH = (
    "math.numbers.fraction-equivalence",
    "math.numbers.proportions",
    "math.relations.first-degree-equations",
    "math.us.algebra.linear-equations",
    "math.us.algebra.quadratic-equations",
    "math.us.trigonometry.triangle-solving",
    "math.us.functions.precalculus-analysis",
    "math.us.scientifico.calculus.optimization",
)

ENGLISH_LICEO_PATH = (
    "eng.grammar.present_simple",
    "eng.grammar.past_regular",
    "eng.grammar.present_perfect_vs_past",
    "eng.us.grammar.tense-control-b1",
    "eng.us.grammar.aspect-b1",
    "eng.us.grammar.complex-sentences-b1plus",
    "eng.us.liceo.writing.b2-argument",
    "eng.us.liceo.integrated.b2-target",
)


@dataclass(frozen=True)
class EightYearProfile:
    name: str
    subject: str
    targets: tuple[str, ...]
    profile_kind: str = "typical"
    initial_skill: float = 0.72
    yearly_gain: float = 0.025
    learning_gain: float = 0.055
    transfer_offset: float = -0.05
    support_dependence: float = 0.15
    volatility: float = 0.07
    gap_stage: int | None = None
    gap_prerequisite: str | None = None
    gap_skill: float | None = None
    deep_gap_prerequisite: str | None = None
    deep_gap_skill: float | None = None
    recovery_gain: float = 0.16


PROFILES_8Y = (
    EightYearProfile(
        "strong_math_scientific", "mathematics", MATH_SCIENTIFIC_PATH,
        profile_kind="strong", initial_skill=0.88, yearly_gain=0.015,
        learning_gain=0.045, transfer_offset=-0.01, volatility=0.035,
    ),
    EightYearProfile(
        "typical_math_scientific", "mathematics", MATH_SCIENTIFIC_PATH,
        initial_skill=0.73, yearly_gain=0.018, learning_gain=0.055,
        transfer_offset=-0.06, volatility=0.065,
    ),
    EightYearProfile(
        "cross_stage_gap_math", "mathematics", MATH_SCIENTIFIC_PATH,
        profile_kind="cross_stage_gap", initial_skill=0.71, yearly_gain=0.018,
        learning_gain=0.055, transfer_offset=-0.08, volatility=0.055,
        gap_stage=4, gap_prerequisite="math.numbers.signed-operations",
        gap_skill=0.34, deep_gap_prerequisite="math.numbers.signed-number-sense",
        deep_gap_skill=0.42, recovery_gain=0.18,
    ),
    EightYearProfile(
        "support_dependent_math", "mathematics", MATH_SCIENTIFIC_PATH,
        profile_kind="support_dependent", initial_skill=0.79, yearly_gain=0.012,
        learning_gain=0.045, transfer_offset=-0.10, support_dependence=0.78,
        volatility=0.05,
    ),
    EightYearProfile(
        "strong_english_liceo", "english", ENGLISH_LICEO_PATH,
        profile_kind="strong", initial_skill=0.88, yearly_gain=0.015,
        learning_gain=0.045, transfer_offset=-0.01, volatility=0.04,
    ),
    EightYearProfile(
        "typical_english_liceo", "english", ENGLISH_LICEO_PATH,
        initial_skill=0.73, yearly_gain=0.018, learning_gain=0.055,
        transfer_offset=-0.05, volatility=0.07,
    ),
    EightYearProfile(
        "cross_stage_gap_english", "english", ENGLISH_LICEO_PATH,
        profile_kind="cross_stage_gap", initial_skill=0.71, yearly_gain=0.018,
        learning_gain=0.055, transfer_offset=-0.07, volatility=0.055,
        gap_stage=4, gap_prerequisite="eng.grammar.present_perfect_vs_past",
        gap_skill=0.36, deep_gap_prerequisite="eng.grammar.past_irregular",
        deep_gap_skill=0.45, recovery_gain=0.17,
    ),
    EightYearProfile(
        "support_dependent_english", "english", ENGLISH_LICEO_PATH,
        profile_kind="support_dependent", initial_skill=0.80, yearly_gain=0.012,
        learning_gain=0.045, transfer_offset=-0.10, support_dependence=0.80,
        volatility=0.055,
    ),
)
