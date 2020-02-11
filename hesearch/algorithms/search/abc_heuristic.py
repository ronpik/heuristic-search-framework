from abc import ABC, abstractmethod

from hesearch.algorithms.search.abc_search import AbstractSearch
from hesearch.framework.problem import SearchState


class AbstractHeuristic(ABC):

    @abstractmethod
    def estimate(self, state: SearchState) -> float:
        return NotImplemented


class AbstractCostSearch(AbstractSearch):

    @abstractmethod
    def evaluate_cost(self, state: SearchState, state_cost: float) -> float:
        """
        evaluate the cost of the given state.
        :param state_cost: the cost of reaching the current state.
        :param state:
        :return: the total cost of state.
        """
        return NotImplemented
