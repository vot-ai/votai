"""Online learning

Online learning updater functions
"""
from typing import Callable, Tuple, Iterable
from numpy import exp
from .types import AnnotatorConfidence, RelevanceScore, Mu, SigmaSquared, Alpha, Beta, C
from .constants import KAPPA


def update_mu(
    winner: RelevanceScore, loser: RelevanceScore, annotator: AnnotatorConfidence
) -> Tuple[RelevanceScore, RelevanceScore]:
    """Update μ

    Applies equations (11) and (12) to compute the updated μ for both the winner and the loser

    Arguments:
        winner {RelevanceScore} -- Winner's current score
        loser {RelevanceScore} -- Loser's current score
        annotator {AnnotatorConfidence} -- Confidence of the annotator

    Returns:
        Tuple[RelevanceScore, RelevanceScore] -- Tuple (Winner, Loser) with updated μ for both
    """

    # Cache computations
    exp_winner_mu: float = exp(winner.mu)
    exp_loser_mu: float = exp(loser.mu)
    alpha_exp_winner_mu = annotator.alpha * exp_winner_mu
    update_factor = (
        alpha_exp_winner_mu / (alpha_exp_winner_mu + annotator.beta * exp_loser_mu)
    ) - (exp_winner_mu / (exp_winner_mu + exp_loser_mu))

    # Compute new winner's and loser's mu
    new_winner_mu = Mu(winner.mu + winner.sigma_squared * update_factor)
    new_loser_mu = Mu(loser.mu - loser.sigma_squared * update_factor)

    # Returne typed results
    return (
        RelevanceScore(new_winner_mu, winner.sigma_squared),
        RelevanceScore(new_loser_mu, loser.sigma_squared),
    )


def update_sigma_squared(
    winner: RelevanceScore, loser: RelevanceScore, annotator: AnnotatorConfidence
) -> Tuple[RelevanceScore, RelevanceScore]:
    """Update σ²

    Applies equations (13) and (14) to compute the updated σ² for both the winner and the loser

    Arguments:
        winner {RelevanceScore} -- Winner's current score
        loser {RelevanceScore} -- Loser's current score
        annotator {AnnotatorConfidence} -- Confidence of the annotator

    Returns:
        Tuple[RelevanceScore, RelevanceScore] -- Tuple(Winner, Loser) with updated σ² for both
    """

    # Cache computations
    exp_winner_mu: float = exp(winner.mu)
    exp_loser_mu: float = exp(loser.mu)
    alpha_exp_winner_mu = annotator.alpha * exp_winner_mu
    beta_exp_loser_mu = annotator.beta * exp_loser_mu
    update_factor = (alpha_exp_winner_mu * beta_exp_loser_mu) / (
        (alpha_exp_winner_mu + beta_exp_loser_mu) ** 2
    ) - (exp_winner_mu * exp_loser_mu) / ((exp_winner_mu + exp_loser_mu) ** 2)

    # Compute new winner's and loser's sigma squared
    new_winner_sigma_squared = SigmaSquared(
        winner.sigma_squared * max(1 + winner.sigma_squared * update_factor, KAPPA)
    )
    new_loser_sigma_squared = SigmaSquared(
        loser.sigma_squared * max(1 + loser.sigma_squared * update_factor, KAPPA)
    )

    # Return typed results
    return (
        RelevanceScore(winner.mu, new_winner_sigma_squared),
        RelevanceScore(loser.mu, new_loser_sigma_squared),
    )


def update_scores(
    winner: RelevanceScore, loser: RelevanceScore, annotator: AnnotatorConfidence
) -> Iterable[RelevanceScore]:
    """Update Scores

    Given the winner, loser and annotator, return updated winner and loser

    Arguments:
        winner {RelevanceScore} -- Winner's current score
        loser {RelevanceScore} -- Loser's current score
        annotator {AnnotatorConfidence} -- Confidence of the annotator

    Returns:
        Iterable[RelevanceScore] -- Updated tuple(Winner, Loser)
    """
    join: Callable[
        [Tuple[RelevanceScore, RelevanceScore]], RelevanceScore
    ] = lambda scores: RelevanceScore(scores[0].mu, scores[1].sigma_squared)
    zipped = zip(
        update_mu(winner, loser, annotator),
        update_sigma_squared(winner, loser, annotator),
    )
    mapped = map(join, zipped)
    return tuple(mapped)


def update_annotator(
    winner: RelevanceScore, loser: RelevanceScore, annotator: AnnotatorConfidence
) -> Tuple[AnnotatorConfidence, C]:
    """Update Annotator

    Applies equations (16) and (17) to updated the annotators ɑ and β

    Arguments:
        winner {RelevanceScore} -- Winner's current score
        loser {RelevanceScore} -- Loser's current score
        annotator {AnnotatorConfidence} -- Current confidence of the annotator

    Returns:
        Tuple[AnnotatorConfidence, C] -- Tuple with the new annotator's confidence and the normalization
        of the operation
    """

    # Extract long variables
    alpha = annotator.alpha
    beta = annotator.beta

    # Cache computations
    exp_winner_mu: float = exp(winner.mu)
    exp_loser_mu: float = exp(loser.mu)

    # Calculate Cs
    c_1 = exp_winner_mu / (exp_winner_mu + exp_loser_mu) + 0.5 * (
        winner.sigma_squared + loser.sigma_squared
    ) * (
        exp_winner_mu
        * exp_loser_mu
        * (exp_loser_mu - exp_winner_mu)
        / (exp_winner_mu + exp_loser_mu) ** 3
    )
    c_2 = 1 - c_1
    c = C((c_1 * alpha + c_2 * beta) / sum(annotator))  # pylint: disable=invalid-name

    # Cache expectations
    expectation = (c_1 * (alpha + 1) * alpha + c_2 * alpha * beta) / (
        c * (sum(annotator) + 1) * sum(annotator)
    )
    expectation_squared = (
        c_1 * (alpha + 2) * (alpha + 1) * alpha + c_2 * (alpha + 1) * alpha * beta
    ) / (c * (sum(annotator) + 2) * (sum(annotator) + 1) * sum(annotator))

    # Compute new alpha and beta
    variance = expectation_squared - expectation ** 2
    new_alpha = Alpha(((expectation - expectation_squared) * expectation) / variance)
    new_beta = Beta(
        ((expectation - expectation_squared) * (1 - expectation)) / variance
    )

    # Return typed results
    return AnnotatorConfidence(new_alpha, new_beta), c


def update(
    winner: RelevanceScore, loser: RelevanceScore, annotator: AnnotatorConfidence
) -> Tuple[RelevanceScore, RelevanceScore, AnnotatorConfidence]:
    """Update decision

    Given a winner, loser and annotator, update all of their parameters and return them to be saved

    Arguments:
        winner {RelevanceScore} -- Winner's current score
        loser {RelevanceScore} -- Loser's current score
        annotator {AnnotatorConfidence} -- Current confidence of the annotator

    Returns:
        Tuple[RelevanceScore, RelevanceScore, AnnotatorConfidence] -- Tuple with new winner, loser and annotator's values
    """
    (new_winner, new_loser) = update_scores(winner, loser, annotator)
    (new_annotator, _) = update_annotator(winner, loser, annotator)

    return new_winner, new_loser, new_annotator
