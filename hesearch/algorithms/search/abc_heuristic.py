from abc import ABC, abstractmethod
from typing import NamedTuple

from hesearch.algorithms.search.abc_search import AbstractSearch
from hesearch.framework.problem import SearchState


class HeuristicEstimator(ABC):

    @abstractmethod
    def estimate(self, state: SearchState) -> float:
        return NotImplemented


class StateContext(NamedTuple):
    state: SearchState
    depth: int
    reaching_cost: float


class CostSearcher(AbstractSearch):

    @abstractmethod
    def evaluate_cost(self, state_context: StateContext) -> float:
        """
        evaluate the cost of the given state.
        :param state_context: contains information regarding the state for which a cost is being evaluated.
        :return: the total cost of the state in the state_context.
        """
        return NotImplemented
