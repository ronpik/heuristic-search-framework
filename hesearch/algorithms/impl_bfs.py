import heapq
from typing import Any, Dict, Callable, Counter

from hesearch.algorithms.cost_search_utils import uniform_cost, basic_heuristic_cost
from hesearch.algorithms.search import HeuristicEstimator
from hesearch.algorithms.search.abc_heuristic import StateContext, HeuristicCostSearcher
from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.algorithms.search.iterative_deepening import BaseIterativeDeepening
from hesearch.framework.analysis.cost_search_analyzer import HeuristicCostSearchAnalyzer


class UniformCostSearch(BaseBFS):

    def evaluate_cost(self, state_context: StateContext) -> float:
        return uniform_cost(state_context)


class AStar(BaseBFS, HeuristicCostSearcher):

    def __init__(self, heuristic: HeuristicEstimator):
        super().__init__()
        self.__h = heuristic

    @property
    def heuristic(self) -> HeuristicEstimator:
        return self.__h

    def evaluate_heuristic_cost(self, state_context: StateContext, heuristic_value: float) -> float:
        return basic_heuristic_cost(state_context.reaching_cost, heuristic_value)






