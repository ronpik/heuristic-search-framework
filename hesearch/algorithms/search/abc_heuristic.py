from abc import ABC, abstractmethod, abstractproperty
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


class HeuristicCostSearcher(CostSearcher):

    @property
    @abstractmethod
    def heuristic(self) -> HeuristicEstimator:
        return NotImplemented

    @abstractmethod
    def evaluate_heuristic_cost(self, state_context: StateContext, heuristic_value: float) -> float:
        return NotImplemented

    def evaluate_cost(self, state_context: StateContext) -> float:
        h = self.heuristic.estimate(state_context.state)
        return self.evaluate_heuristic_cost(state_context, h)
