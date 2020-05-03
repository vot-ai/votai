from typing import Callable, Sequence, TypeVar
from random import sample
import numpy as np
from scipy.special import psi, beta  # pylint: disable=no-name-in-module
from .types import RelevanceScore, AnnotatorConfidence

T = TypeVar("T")  # pylint: disable=invalid-name

log: Callable[[float], float] = np.log
typed_beta: Callable[[float, float], float] = beta
typed_psi: Callable[[float], float] = psi


def random_argmax(__func: Callable[[T], float], __iter: Sequence[T]) -> T:
    """Random Argmax

    Given an iterable and a function, return the value that produces the maximum output
    when applied to the function.

    Shuffles input iterable so draws are randomly selected

    Arguments:
        __func {Callable[[T], float]} -- Maximization function
        __iter {Iterable[T]} -- Iterable of values to be maximized

    Returns:
        T -- Element of the iterable that produced the maximum
    """
    return max(sample(__iter, len(__iter)), key=__func)


def gaussian_relative_entropy(score1: RelevanceScore, score2: RelevanceScore) -> float:
    """Gaussian Kullback–Leibler divergence

    Relative Entropy utility function for gaussian distributions
    """
    sigma_ratio = score1.sigma_squared / score2.sigma_squared
    return (score1.mu - score2.mu) ** 2 / (2 * score2.sigma_squared) + (
        sigma_ratio - 1 - log(sigma_ratio)
    ) / 2


def beta_relative_entropy(
    conf1: AnnotatorConfidence, conf2: AnnotatorConfidence
) -> float:
    """Beta Kullback–Leibler divergence

    Relative Entropy utility function for beta distributions
    """
    return (
        log(typed_beta(*conf2) / typed_beta(*conf1))
        + (conf1.alpha - conf2.alpha) * typed_psi(conf1.alpha)
        + (conf1.beta - conf2.beta) * typed_psi(conf1.beta)
        + (conf2.alpha - conf1.alpha + conf2.beta - conf1.beta) * typed_psi(sum(conf1))
    )
