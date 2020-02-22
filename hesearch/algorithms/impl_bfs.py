import heapq
from typing import Any, Dict, Callable

from hesearch.algorithms.search import HeuristicEstimator
from hesearch.algorithms.search.abc_heuristic import StateContext, HeuristicCostSearcher
from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.algorithms.search.iterative_deepening import BaseIterativeDeepening
from hesearch.framework.analysis.cost_search_analyzer import HeuristicCostSearchAnalyzer
from hesearch.framework.problem import SearchSpace, SearchState


def uniform_cost(state_context: StateContext):
    return state_context.reaching_cost


def basic_heuristic_cost(g: float, h: float):
    return g + h


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


class IDDFS(BaseIterativeDeepening):

    def evaluate_cost(self, state_context: StateContext) -> float:
        return uniform_cost(state_context)


class IDAStar(BaseIterativeDeepening, HeuristicCostSearcher):

    def __init__(self, heuristic: HeuristicEstimator):
        super().__init__()
        self.__h = heuristic

    @property
    def heuristic(self) -> HeuristicEstimator:
        return self.__h

    def evaluate_heuristic_cost(self, state_context: StateContext, heuristic_value: float) -> float:
        return basic_heuristic_cost(state_context.reaching_cost, heuristic_value)


class HeuristicBFSCostSearchAnalyzer(BaseBFS, HeuristicCostSearchAnalyzer):
    def __init__(self, cost_search_algo: HeuristicCostSearcher, name: str):
        BaseBFS.__init__(self)
        HeuristicCostSearchAnalyzer.__init__(self, cost_search_algo, name)


class HeuristicIDCostSearchAnalyzer(BaseIterativeDeepening, HeuristicCostSearchAnalyzer):
    def __init__(self, cost_search_algo: HeuristicCostSearcher, name: str):
        BaseIterativeDeepening.__init__(self)
        HeuristicCostSearchAnalyzer.__init__(self, cost_search_algo, name)