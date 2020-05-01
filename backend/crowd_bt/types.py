from typing import NewType, NamedTuple


"""Mu

Given a relevance score (s), its Gaussian-distributed format is given by:
s ~ N(μ, σ²)
"""
Mu = NewType("μ", float)


"""Sigma Squared

Given a relevance score (s), its Gaussian-distributed format is given by:
s ~ N(μ, σ²)
"""
SigmaSquared = NewType("σ²", float)


class RelevanceScore(NamedTuple):
    """Relevance Score (s)

    Score that evaluates how relevant an item is according to annotators
    
    Represented as a Gaussian-distributed random variable with parameters μ and σ²
    such that:
        s ~ N(μ, σ²)
    """

    mu: Mu
    sigma_squared: SigmaSquared


Alpha = NewType("α", float)

Beta = NewType("β", float)


class AnnotatorConfidence(NamedTuple):
    """Annotator Confidence (η)

    Probability that an annotator agrees with the true pairwise preference

    Represented as a Beta-distributed random variable with parameters α and β,
    such that:
        η ~ Beta(α, β)
    """

    alpha: Alpha
    beta: Beta


C = NewType("Normalization Constant", float)
