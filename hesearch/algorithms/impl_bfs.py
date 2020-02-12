import heapq
from typing import Any, Dict, Callable

from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.algorithms.search.iterative_deepening import BaseIterativeDeepening
from hesearch.framework.problem import SearchSpace, SearchState


class UniformCostSearch(BaseBFS):

    def evaluate_cost(self, state: SearchState, state_cost: float) -> float:
        return state_cost


class AStar(BaseBFS):

    def __init__(self, heuristic_func: Callable[[SearchState], float]):
        super().__init__()
        self.__h = heuristic_func

    def evaluate_cost(self, state: SearchState, state_cost: float) -> float:
        g = state_cost
        h = self.__h(state)
        return g + h


class IDDFS(BaseIterativeDeepening):

    def evaluate_cost(self, state: SearchState, state_cost: float) -> float:
        return state_cost


class IDAStar(BaseIterativeDeepening):

    def __init__(self, heuristic_func: Callable[[SearchState], float]):
        super().__init__()
        self.__h = heuristic_func

    def evaluate_cost(self, state: SearchState, state_cost: float) -> float:
        g = state_cost
        h = self.__h(state)
        return g + h
