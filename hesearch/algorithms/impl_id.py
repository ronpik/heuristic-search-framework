from collections import Counter

from hesearch.algorithms.cost_search_utils import uniform_cost, basic_heuristic_cost
from hesearch.algorithms.search.abc_heuristic import StateContext, HeuristicCostSearcher, HeuristicEstimator
from hesearch.algorithms.search.iterative_deepening import BaseIterativeDeepening

class IDDFS(BaseIterativeDeepening):

    def evaluate_cost(self, state_context: StateContext) -> float:
        return uniform_cost(state_context)


class IDAStar(BaseIterativeDeepening, HeuristicCostSearcher):

    def _calculate_next_bound(self) -> float:
        pass

    def __init__(self, heuristic: HeuristicEstimator):
        super().__init__()
        self.__h = heuristic

    @property
    def heuristic(self) -> HeuristicEstimator:
        return self.__h

    def evaluate_heuristic_cost(self, state_context: StateContext, heuristic_value: float) -> float:
        return basic_heuristic_cost(state_context.reaching_cost, heuristic_value)


class SIDAStar(BaseIterativeDeepening, HeuristicCostSearcher):

    def __init__(self, heuristic: HeuristicEstimator):
        super().__init__()
        self.__h = heuristic

        self.all_h_values = Counter
        self.open_h_values = Counter

    @property
    def heuristic(self) -> HeuristicEstimator:
        return self.__h

    def evaluate_heuristic_cost(self, state_context: StateContext, heuristic_value: float) -> float:
        self.all_h_values[heuristic_value] += 1
        self.open_h_values[heuristic_value] += 1
        return basic_heuristic_cost(state_context.reaching_cost, heuristic_value)

    def _calculate_next_bound(self) -> float:
        return self.min_above_bound

