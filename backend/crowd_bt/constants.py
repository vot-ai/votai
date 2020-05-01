from typing import Final

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
