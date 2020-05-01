from typing import Callable, Iterable
import numpy as np
from scipy.special import psi, beta
from .types import RelevanceScore, AnnotatorConfidence


def gaussian_relative_entropy(score1: RelevanceScore, score2: RelevanceScore) -> float:
    """Gaussian Kullback–Leibler divergence

    Relative Entropy utility function for gaussian distributions
    """
    sigma_ratio = score1.sigma_squared / score2.sigma_squared
    return (score1.mu - score2.mu) ** 2 / (2 * score2.sigma_squared) + (
        sigma_ratio - 1 - np.log(sigma_ratio)
    ) / 2


def beta_relative_entropy(
    conf1: AnnotatorConfidence, conf2: AnnotatorConfidence
) -> float:
    """Beta Kullback–Leibler divergence

    Relative Entropy utility function for beta distributions
    """
    return (
        np.log(beta(*conf2) / beta(*conf1))
        + (conf1.alpha - conf2.alpha) * psi(conf1.alpha)
        + (conf1.beta - conf2.beta) * psi(conf1.beta)
        + (conf2.alpha - conf1.alpha + conf2.beta - conf1.beta) * psi(sum(conf1))
    )
