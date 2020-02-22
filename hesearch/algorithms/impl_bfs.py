import heapq
from typing import Any, Dict, Callable

from hesearch.algorithms.search import HeuristicEstimator
from hesearch.algorithms.search.abc_heuristic import StateContext
from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.algorithms.search.iterative_deepening import BaseIterativeDeepening
from hesearch.framework.problem import SearchSpace, SearchState


def uniform_cost(state_context: StateContext):
    return state_context.reaching_cost


def heuristic_cost(state_context: StateContext, heuristic: Callable[[SearchState], float]):
    g = state_context.reaching_cost
    h = heuristic(state_context.state)
    return g + h


class UniformCostSearch(BaseBFS):

    def evaluate_cost(self, state_context: StateContext) -> float:
        return uniform_cost(state_context)


class AStar(BaseBFS):

    def __init__(self, heuristic: HeuristicEstimator):
        super().__init__()
        self.__h = heuristic.estimate

    def evaluate_cost(self, state_context: StateContext) -> float:
        return heuristic_cost(state_context, self.__h)


class IDDFS(BaseIterativeDeepening):

    def evaluate_cost(self, state_context: StateContext) -> float:
        return uniform_cost(state_context)


class IDAStar(BaseIterativeDeepening):

    def __init__(self, heuristic: HeuristicEstimator):
        super().__init__()
        self.__h = heuristic.estimate

    def evaluate_cost(self, state_context: StateContext) -> float:
        return heuristic_cost(state_context, self.__h)

