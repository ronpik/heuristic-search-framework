from typing import List

from hesearch.algorithms.search.abc_heuristic import CostSearcher, StateContext, HeuristicEstimator
from hesearch.framework.problem import SearchState, SearchSpace


class CostSearchAnalyzer(CostSearcher):

    def __init__(self, cost_search_algo: CostSearcher, heuristic: HeuristicEstimator):
        self.searcher = cost_search_algo
        self.heuristic = heuristic

    def evaluate_cost(self, state_context: StateContext) -> float:
        pass



    def set_search_space(self, search_space: SearchSpace):
        self.searcher.set_search_space(search_space)

    def search(self):
        self.searcher.search()

    def get_optimal_cost(self) -> float:
        return self.searcher.get_optimal_cost()

    def get_optimal_path(self) -> List[SearchState]:
        return self.searcher.get_optimal_path()