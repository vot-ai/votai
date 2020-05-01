import itertools
from typing import Any, Iterable
import unittest
from numpy.random import permutation
from crowd_bt import utils, online, entropy
from crowd_bt.types import RelevanceScore, AnnotatorConfidence, Mu, SigmaSquared, Alpha, Beta


def combine(*arrays):
    return tuple(itertools.product(*arrays))

def extract(elements, index):
    return tuple(map(lambda x: x[index], elements))


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.scores = [
            RelevanceScore(Mu(2.0), SigmaSquared(2.0)),
            RelevanceScore(Mu(4.0), SigmaSquared(1.0)),
            RelevanceScore(Mu(3.0), SigmaSquared(0.5)),
        ]
        
        self.annotators = [
            AnnotatorConfidence(Alpha(5), Beta(2)),
            AnnotatorConfidence(Alpha(2), Beta(5)),
            AnnotatorConfidence(Alpha(1), Beta(2)),
        ]
    
    def test_gaussian_relative_entropy(self):
        combinations = combine(self.scores, self.scores)
        solutions = [0.0, 2.1534264097200273, 1.8068528194400546, 1.0965735902799727, 0.0, 1.1534264097200273, 0.5681471805599453, 0.5965735902799727, 0.0]
        for comb, solution in zip(combinations, solutions):
            self.assertEqual(utils.gaussian_relative_entropy(*comb), solution)

    def test_beta_relative_entropy(self):
        combinations = combine(self.annotators, self.annotators)
        solutions = [0.0, 3.2499999999999996, 1.2413835344355437, 3.2499999999999996, 0.0, 0.1580502011022098, 3.29194979889779, 0.29194979889778994, 0.0]
        for comb, solution in zip(combinations, solutions):
            self.assertEqual(utils.beta_relative_entropy(*comb), solution)


class OnlineTestCase(unittest.TestCase):
    def setUp(self):
        self.scores = [
            RelevanceScore(Mu(2.0), SigmaSquared(2.0)),
            RelevanceScore(Mu(4.0), SigmaSquared(1.0)),
            RelevanceScore(Mu(3.0), SigmaSquared(0.5)),
        ]
        
        self.annotators = [
            AnnotatorConfidence(Alpha(5), Beta(2)),
            AnnotatorConfidence(Alpha(2), Beta(5)),
            AnnotatorConfidence(Alpha(1), Beta(2)),
        ]
    
    def test_update_mu(self):
        combinations = combine(self.scores, self.scores, self.annotators)
        solutions = [(RelevanceScore(mu=2.428571428571429, sigma_squared=2.0), RelevanceScore(mu=1.5714285714285714, sigma_squared=2.0)), (RelevanceScore(mu=1.5714285714285714, sigma_squared=2.0), RelevanceScore(mu=2.428571428571429, sigma_squared=2.0)), (RelevanceScore(mu=1.6666666666666667, sigma_squared=2.0), RelevanceScore(mu=2.333333333333333, sigma_squared=2.0)), (RelevanceScore(mu=2.2672035841943887, sigma_squared=2.0), RelevanceScore(mu=3.866398207902806, sigma_squared=1.0)), (RelevanceScore(mu=1.8643023647347248, sigma_squared=2.0), RelevanceScore(mu=4.067848817632638, sigma_squared=1.0)), (RelevanceScore(mu=1.8883520326218401, sigma_squared=2.0), RelevanceScore(mu=4.05582398368908, sigma_squared=1.0)), (RelevanceScore(mu=2.4202869465441763, sigma_squared=2.0), RelevanceScore(mu=2.8949282633639557, sigma_squared=0.5)), (RelevanceScore(mu=1.718668695577935, sigma_squared=2.0), RelevanceScore(mu=3.0703328261055165, sigma_squared=0.5)), (RelevanceScore(mu=1.772841964253937, sigma_squared=2.0), RelevanceScore(mu=3.056789508936516, sigma_squared=0.5)), (RelevanceScore(mu=4.067848817632638, sigma_squared=1.0), RelevanceScore(mu=1.8643023647347245, sigma_squared=2.0)), (RelevanceScore(mu=3.866398207902806, sigma_squared=1.0), RelevanceScore(mu=2.2672035841943883, sigma_squared=2.0)), (RelevanceScore(mu=3.906188964183716, sigma_squared=1.0), RelevanceScore(mu=2.187622071632568, sigma_squared=2.0)), (RelevanceScore(mu=4.214285714285714, sigma_squared=1.0), RelevanceScore(mu=3.7857142857142856, sigma_squared=1.0)), (RelevanceScore(mu=3.7857142857142856, sigma_squared=1.0), RelevanceScore(mu=4.214285714285714, sigma_squared=1.0)), (RelevanceScore(mu=3.8333333333333335, sigma_squared=1.0), RelevanceScore(mu=4.166666666666667, sigma_squared=1.0)), (RelevanceScore(mu=4.140665652211033, sigma_squared=1.0), RelevanceScore(mu=2.9296671738944835, sigma_squared=0.5)), (RelevanceScore(mu=3.789856526727912, sigma_squared=1.0), RelevanceScore(mu=3.1050717366360443, sigma_squared=0.5)), (RelevanceScore(mu=3.845058306135824, sigma_squared=1.0), RelevanceScore(mu=3.077470846932088, sigma_squared=0.5)), (RelevanceScore(mu=3.0703328261055165, sigma_squared=0.5), RelevanceScore(mu=1.7186686955779347, sigma_squared=2.0)), (RelevanceScore(mu=2.8949282633639557, sigma_squared=0.5), RelevanceScore(mu=2.4202869465441763, sigma_squared=2.0)), (RelevanceScore(mu=2.922529153067912, sigma_squared=0.5), RelevanceScore(mu=2.3098833877283513, sigma_squared=2.0)), (RelevanceScore(mu=3.1050717366360443, sigma_squared=0.5), RelevanceScore(mu=3.789856526727912, sigma_squared=1.0)), (RelevanceScore(mu=2.9296671738944835, sigma_squared=0.5), RelevanceScore(mu=4.140665652211033, sigma_squared=1.0)), (RelevanceScore(mu=2.943210491063484, sigma_squared=0.5), RelevanceScore(mu=4.113579017873032, sigma_squared=1.0)), (RelevanceScore(mu=3.107142857142857, sigma_squared=0.5), RelevanceScore(mu=2.892857142857143, sigma_squared=0.5)), (RelevanceScore(mu=2.892857142857143, sigma_squared=0.5), RelevanceScore(mu=3.107142857142857, sigma_squared=0.5)), (RelevanceScore(mu=2.9166666666666665, sigma_squared=0.5), RelevanceScore(mu=3.0833333333333335, sigma_squared=0.5))]
        for comb, solution in zip(combinations, solutions):
            self.assertEqual(online.update_mu(*comb), solution)
        
    def test_update_sigma(self):
        combinations = combine(self.scores, self.scores, self.annotators)
        solutions = [(RelevanceScore(mu=2.0, sigma_squared=1.816326530612245), RelevanceScore(mu=2.0, sigma_squared=1.816326530612245)), (RelevanceScore(mu=2.0, sigma_squared=1.816326530612245), RelevanceScore(mu=2.0, sigma_squared=1.816326530612245)), (RelevanceScore(mu=2.0, sigma_squared=1.888888888888889), RelevanceScore(mu=2.0, sigma_squared=1.888888888888889)), (RelevanceScore(mu=2.0, sigma_squared=2.3356036209394335), RelevanceScore(mu=4.0, sigma_squared=1.0839009052348583)), (RelevanceScore(mu=2.0, sigma_squared=1.7748930997933112), RelevanceScore(mu=4.0, sigma_squared=0.9437232749483279)), (RelevanceScore(mu=2.0, sigma_squared=1.8174738524212324), RelevanceScore(mu=4.0, sigma_squared=0.9543684631053081)), (RelevanceScore(mu=2.0, sigma_squared=2.2118025005055415), RelevanceScore(mu=3.0, sigma_squared=0.5132376562815963)), (RelevanceScore(mu=2.0, sigma_squared=1.660836651856629), RelevanceScore(mu=3.0, sigma_squared=0.4788022907410393)), (RelevanceScore(mu=2.0, sigma_squared=1.7384519753405139), RelevanceScore(mu=3.0, sigma_squared=0.4836532484587821)), (RelevanceScore(mu=4.0, sigma_squared=0.9437232749483279), RelevanceScore(mu=2.0, sigma_squared=1.7748930997933112)), (RelevanceScore(mu=4.0, sigma_squared=1.0839009052348583), RelevanceScore(mu=2.0, sigma_squared=2.3356036209394335)), (RelevanceScore(mu=4.0, sigma_squared=1.0626454262009146), RelevanceScore(mu=2.0, sigma_squared=2.2505817048036585)), (RelevanceScore(mu=4.0, sigma_squared=0.9540816326530612), RelevanceScore(mu=4.0, sigma_squared=0.9540816326530612)), (RelevanceScore(mu=4.0, sigma_squared=0.9540816326530612), RelevanceScore(mu=4.0, sigma_squared=0.9540816326530612)), (RelevanceScore(mu=4.0, sigma_squared=0.9722222222222222), RelevanceScore(mu=4.0, sigma_squared=0.9722222222222222)), (RelevanceScore(mu=4.0, sigma_squared=0.9152091629641572), RelevanceScore(mu=3.0, sigma_squared=0.4788022907410393)), (RelevanceScore(mu=4.0, sigma_squared=1.0529506251263854), RelevanceScore(mu=3.0, sigma_squared=0.5132376562815963)), (RelevanceScore(mu=4.0, sigma_squared=1.0475942866120638), RelevanceScore(mu=3.0, sigma_squared=0.5118985716530159)), (RelevanceScore(mu=3.0, sigma_squared=0.4788022907410393), RelevanceScore(mu=2.0, sigma_squared=1.660836651856629)), (RelevanceScore(mu=3.0, sigma_squared=0.5132376562815963), RelevanceScore(mu=2.0, sigma_squared=2.2118025005055415)), (RelevanceScore(mu=3.0, sigma_squared=0.5118985716530159), RelevanceScore(mu=2.0, sigma_squared=2.190377146448255)), (RelevanceScore(mu=3.0, sigma_squared=0.5132376562815963), RelevanceScore(mu=4.0, sigma_squared=1.0529506251263854)), (RelevanceScore(mu=3.0, sigma_squared=0.4788022907410393), RelevanceScore(mu=4.0, sigma_squared=0.9152091629641572)), (RelevanceScore(mu=3.0, sigma_squared=0.4836532484587821), RelevanceScore(mu=4.0, sigma_squared=0.9346129938351284)), (RelevanceScore(mu=3.0, sigma_squared=0.4885204081632653), RelevanceScore(mu=3.0, sigma_squared=0.4885204081632653)), (RelevanceScore(mu=3.0, sigma_squared=0.4885204081632653), RelevanceScore(mu=3.0, sigma_squared=0.4885204081632653)), (RelevanceScore(mu=3.0, sigma_squared=0.4930555555555556), RelevanceScore(mu=3.0, sigma_squared=0.4930555555555556))]
        for comb, solution in zip(combinations, solutions):
            for el1, el2 in zip(online.update_sigma_squared(*comb), solution):
                self.assertEqual(el1, el2)
    
    def test_update_annotator(self):
        combinations = combine(self.scores, self.scores, self.annotators)
        solutions = [(AnnotatorConfidence(alpha=5.000000000000006, beta=2.0000000000000027), 0.5), (AnnotatorConfidence(alpha=1.9999999999999996, beta=4.999999999999999), 0.5), (AnnotatorConfidence(alpha=1.0, beta=2.0000000000000004), 0.5), (AnnotatorConfidence(alpha=4.681168202339644, beta=2.202874855126965), 0.3882057172598631), (AnnotatorConfidence(alpha=1.9691437898667485, beta=5.490850442654051), 0.6117942827401368), (AnnotatorConfidence(alpha=0.9567633616149619, beta=2.4126765341275953), 0.5869511087978843), (AnnotatorConfidence(alpha=4.822374792369565, beta=2.05734758044722), 0.4496486882690774), (AnnotatorConfidence(alpha=1.974097493318637, beta=5.2090702813962775), 0.5503513117309227), (AnnotatorConfidence(alpha=0.9668015828624185, beta=2.160775229167893), 0.5391621313462731), (AnnotatorConfidence(alpha=5.490850442654117, beta=1.969143789866771), 0.6117942827401368), (AnnotatorConfidence(alpha=2.202874855126978, beta=4.6811682023396735), 0.3882057172598631), (AnnotatorConfidence(alpha=1.2154713317384027, beta=1.796823183436635), 0.41304889120211574), (AnnotatorConfidence(alpha=5.000000000000006, beta=2.0000000000000027), 0.5), (AnnotatorConfidence(alpha=1.9999999999999996, beta=4.999999999999999), 0.5), (AnnotatorConfidence(alpha=1.0, beta=2.0000000000000004), 0.5), (AnnotatorConfidence(alpha=5.295753128041881, beta=1.9699225922912953), 0.5698208290894115), (AnnotatorConfidence(alpha=2.091979072640563, beta=4.766148536889979), 0.43017917091058855), (AnnotatorConfidence(alpha=1.1018336673245, beta=1.8446562805166242), 0.4456949107082355), (AnnotatorConfidence(alpha=5.209070281396275, beta=1.9740974933186355), 0.5503513117309226), (AnnotatorConfidence(alpha=2.0573475804472308, beta=4.822374792369592), 0.44964868826907745), (AnnotatorConfidence(alpha=1.0648480964067388, beta=1.8794858667216199), 0.4608378686537269), (AnnotatorConfidence(alpha=4.766148536889969, beta=2.0919790726405596), 0.4301791709105884), (AnnotatorConfidence(alpha=1.9699225922912922, beta=5.295753128041871), 0.5698208290894116), (AnnotatorConfidence(alpha=0.9603885718783582, beta=2.2337010666605837), 0.5543050892917646), (AnnotatorConfidence(alpha=5.000000000000006, beta=2.0000000000000027), 0.5), (AnnotatorConfidence(alpha=1.9999999999999996, beta=4.999999999999999), 0.5), (AnnotatorConfidence(alpha=1.0, beta=2.0000000000000004), 0.5)]
        for comb, solution in zip(combinations, solutions):
            for el1, el2 in zip(online.update_annotator(*comb), solution):
                self.assertEqual(el1, el2)
    
    def test_update_scores(self):
        combinations = combine(self.scores, self.scores, self.annotators)
        solutions = [(RelevanceScore(mu=2.428571428571429, sigma_squared=1.816326530612245), RelevanceScore(mu=1.5714285714285714, sigma_squared=1.816326530612245)), (RelevanceScore(mu=1.5714285714285714, sigma_squared=1.816326530612245), RelevanceScore(mu=2.428571428571429, sigma_squared=1.816326530612245)), (RelevanceScore(mu=1.6666666666666667, sigma_squared=1.888888888888889), RelevanceScore(mu=2.333333333333333, sigma_squared=1.888888888888889)), (RelevanceScore(mu=2.2672035841943887, sigma_squared=2.3356036209394335), RelevanceScore(mu=3.866398207902806, sigma_squared=1.0839009052348583)), (RelevanceScore(mu=1.8643023647347248, sigma_squared=1.7748930997933112), RelevanceScore(mu=4.067848817632638, sigma_squared=0.9437232749483279)), (RelevanceScore(mu=1.8883520326218401, sigma_squared=1.8174738524212324), RelevanceScore(mu=4.05582398368908, sigma_squared=0.9543684631053081)), (RelevanceScore(mu=2.4202869465441763, sigma_squared=2.2118025005055415), RelevanceScore(mu=2.8949282633639557, sigma_squared=0.5132376562815963)), (RelevanceScore(mu=1.718668695577935, sigma_squared=1.660836651856629), RelevanceScore(mu=3.0703328261055165, sigma_squared=0.4788022907410393)), (RelevanceScore(mu=1.772841964253937, sigma_squared=1.7384519753405139), RelevanceScore(mu=3.056789508936516, sigma_squared=0.4836532484587821)), (RelevanceScore(mu=4.067848817632638, sigma_squared=0.9437232749483279), RelevanceScore(mu=1.8643023647347245, sigma_squared=1.7748930997933112)), (RelevanceScore(mu=3.866398207902806, sigma_squared=1.0839009052348583), RelevanceScore(mu=2.2672035841943883, sigma_squared=2.3356036209394335)), (RelevanceScore(mu=3.906188964183716, sigma_squared=1.0626454262009146), RelevanceScore(mu=2.187622071632568, sigma_squared=2.2505817048036585)), (RelevanceScore(mu=4.214285714285714, sigma_squared=0.9540816326530612), RelevanceScore(mu=3.7857142857142856, sigma_squared=0.9540816326530612)), (RelevanceScore(mu=3.7857142857142856, sigma_squared=0.9540816326530612), RelevanceScore(mu=4.214285714285714, sigma_squared=0.9540816326530612)), (RelevanceScore(mu=3.8333333333333335, sigma_squared=0.9722222222222222), RelevanceScore(mu=4.166666666666667, sigma_squared=0.9722222222222222)), (RelevanceScore(mu=4.140665652211033, sigma_squared=0.9152091629641572), RelevanceScore(mu=2.9296671738944835, sigma_squared=0.4788022907410393)), (RelevanceScore(mu=3.789856526727912, sigma_squared=1.0529506251263854), RelevanceScore(mu=3.1050717366360443, sigma_squared=0.5132376562815963)), (RelevanceScore(mu=3.845058306135824, sigma_squared=1.0475942866120638), RelevanceScore(mu=3.077470846932088, sigma_squared=0.5118985716530159)), (RelevanceScore(mu=3.0703328261055165, sigma_squared=0.4788022907410393), RelevanceScore(mu=1.7186686955779347, sigma_squared=1.660836651856629)), (RelevanceScore(mu=2.8949282633639557, sigma_squared=0.5132376562815963), RelevanceScore(mu=2.4202869465441763, sigma_squared=2.2118025005055415)), (RelevanceScore(mu=2.922529153067912, sigma_squared=0.5118985716530159), RelevanceScore(mu=2.3098833877283513, sigma_squared=2.190377146448255)), (RelevanceScore(mu=3.1050717366360443, sigma_squared=0.5132376562815963), RelevanceScore(mu=3.789856526727912, sigma_squared=1.0529506251263854)), (RelevanceScore(mu=2.9296671738944835, sigma_squared=0.4788022907410393), RelevanceScore(mu=4.140665652211033, sigma_squared=0.9152091629641572)), (RelevanceScore(mu=2.943210491063484, sigma_squared=0.4836532484587821), RelevanceScore(mu=4.113579017873032, sigma_squared=0.9346129938351284)), (RelevanceScore(mu=3.107142857142857, sigma_squared=0.4885204081632653), RelevanceScore(mu=2.892857142857143, sigma_squared=0.4885204081632653)), (RelevanceScore(mu=2.892857142857143, sigma_squared=0.4885204081632653), RelevanceScore(mu=3.107142857142857, sigma_squared=0.4885204081632653)), (RelevanceScore(mu=2.9166666666666665, sigma_squared=0.4930555555555556), RelevanceScore(mu=3.0833333333333335, sigma_squared=0.4930555555555556))]
        for comb, solution in zip(combinations, solutions):
            self.assertEqual(online.update_scores(*comb), solution)



class EntropyTestCase(unittest.TestCase):
    def setUp(self):
        self.scores = [
            RelevanceScore(Mu(2.0), SigmaSquared(2.0)),
            RelevanceScore(Mu(4.0), SigmaSquared(1.0)),
            RelevanceScore(Mu(3.0), SigmaSquared(0.5)),
        ]
        
        self.annotators = [
            AnnotatorConfidence(Alpha(5), Beta(2)),
            AnnotatorConfidence(Alpha(2), Beta(5)),
            AnnotatorConfidence(Alpha(1), Beta(2)),
        ]

    def test_expected_information_gain(self):
        combinations = combine(self.scores, self.scores, self.annotators)
        solutions = [0.09633110893843251, 0.0963311089384234, 0.057158413839948546, 0.09456860905567117, 0.09456860905566827, 0.17723334230821597, 0.05883322039257656, 0.05883322039257659, 0.05888111591013173, 0.09456860905567117, 0.09456860905566827, 0.17723334230821597, 0.04700604237593102, 0.0470060423759219, 0.028170876966696345, 0.052423825081024375, 0.05242382508102336, 0.07763355353531115, 0.05883322039257656, 0.05883322039257659, 0.05888111591013173, 0.052423825081024375, 0.05242382508102336, 0.07763355353531115, 0.023226850609816944, 0.023226850609807826, 0.013986241974739938]
        for comb, solution in zip(combinations, solutions):
            self.assertEqual(entropy.expected_information_gain(*comb), solution)
