from collections import Counter

from hesearch.algorithms.search import HeuristicEstimator
from hesearch.framework.problem import SearchState


class HeuristicEstimatorAnalysisWrapper(HeuristicEstimator):

    def __init__(self, heuristic_estimator: HeuristicEstimator, logging_gap: int = 100):
        self.heuristic = heuristic_estimator

        self.total_distibution = Counter()
        self.logging_gap = logging_gap
        self.print_count = 0

    def estimate(self, state: SearchState) -> float:
        h = self.heuristic.estimate(state)
        self.__index_info(h, state)
        return h

    def __index_info(self, heuristic_value: float, state: SearchState):
        pass