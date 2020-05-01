from .types import AnnotatorConfidence, Mu, RelevanceScore
from .utils import gaussian_relative_entropy, beta_relative_entropy
from .online import update_annotator, update_scores
from .constants import GAMMA


def expected_information_gain(
    score_a: RelevanceScore,
    score_b: RelevanceScore,
    annotator: AnnotatorConfidence,
    gamma: float = GAMMA,
) -> float:
    # Compute results for score_a being the winner and its updated annotator
    (a_winner_score_a, a_winner_score_b) = update_scores(score_a, score_b, annotator)
    a_winner_annotator, a_winner_c = update_annotator(score_a, score_b, annotator)

    # Compute results for score_b being the winner and its updated annotator
    (b_winner_score_b, b_winner_score_a) = update_scores(score_b, score_a, annotator)
    b_winner_annotator, b_winner_c = update_annotator(score_b, score_a, annotator)

    return a_winner_c * (
        gaussian_relative_entropy(a_winner_score_a, score_a)
        + gaussian_relative_entropy(a_winner_score_b, score_b)
        + gamma * beta_relative_entropy(a_winner_annotator, annotator)
    ) + b_winner_c * (
        gaussian_relative_entropy(b_winner_score_a, score_a)
        + gaussian_relative_entropy(b_winner_score_b, score_b)
        + gamma * beta_relative_entropy(b_winner_annotator, annotator)
    )
