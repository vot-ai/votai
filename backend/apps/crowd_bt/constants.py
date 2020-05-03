from typing import Final

# pylint: disable=pointless-string-statement
"""Kappa (κ)

Used by equation (13) and (14)

Ensures positivity of the variance
"""
KAPPA: Final[float] = 1e-4

"""Gamma (Ɣ)

Used by equations (9) and (10)

Represents the tradeoff between exploration and exploitation
"""
GAMMA: Final[float] = 5.0

"""Epsilon (ε)

ε-greedy variable to select random item from pool instead
of the one that maximizes information gain
"""
EPSILON: Final[float] = 0.25

"""Initial Mu (μ)

Initial value for object's μ
"""
MU: Final[float] = 0.0

"""Initial Sigma Squared (σ²)

Initial value for object's σ²
"""
SIGMA_SQUARED: Final[float] = 1.0

"""Initial Alpha (ɑ)

Initial ɑ. Assumes annotator is good.
"""
ALPHA: Final[float] = 10

"""Initial Beta (β)

Initial β. Assumes annotator is good.
"""
BETA: Final[float] = 1
