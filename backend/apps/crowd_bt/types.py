from typing import NewType, NamedTuple


# pylint: disable=pointless-string-statement
"""Mu

Given a relevance score (s), its Gaussian-distributed format is given by:
s ~ N(μ, σ²)
"""
Mu = NewType("Mu", float)


"""Sigma Squared

Given a relevance score (s), its Gaussian-distributed format is given by:
s ~ N(μ, σ²)
"""
SigmaSquared = NewType("SigmaSquared", float)


"""Alpha

Given the probability that the annotator agrees with the true pairwise preferences(η),
we assume it to be a Beta-distributed random variable with parameters α and β:
η ∼ Beta(α, β)
"""
Alpha = NewType("Alpha", float)

"""Beta

Given the probability that the annotator agrees with the true pairwise preferences(η),
we assume it to be a Beta-distributed random variable with parameters α and β:
η ∼ Beta(α, β)
"""
Beta = NewType("Beta", float)

"""Normalization Constant

Normalization constant used to regulate the expected information gain.
"""
C = NewType("C", float)  # pylint: disable=invalid-name


class RelevanceScore(NamedTuple):
    """Relevance Score (s)

    Score that evaluates how relevant an item is according to annotators

    Represented as a Gaussian-distributed random variable with parameters μ and σ²
    such that:
        s ~ N(μ, σ²)
    """

    mu: Mu
    sigma_squared: SigmaSquared


class AnnotatorConfidence(NamedTuple):
    """Annotator Confidence (η)

    Probability that an annotator agrees with the true pairwise preference

    Represented as a Beta-distributed random variable with parameters α and β,
    such that:
        η ~ Beta(α, β)
    """

    alpha: Alpha
    beta: Beta
