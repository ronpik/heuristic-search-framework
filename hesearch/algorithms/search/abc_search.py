from abc import ABC, abstractmethod
from typing import List, Tuple

from hesearch.framework.problem import SearchState, SearchSpace


class AbstractSearch(ABC):

    @abstractmethod
    def set_search_space(self, search_space: SearchSpace):
        """
        prepare a new search space to search for some goal.
        :param search_space:
        :return:
        """
        return NotImplemented

    @abstractmethod
    def search(self):
        """
        perform search over a search state that was set.
        :return:
        """
        return NotImplemented

    @abstractmethod
    def get_optimal_cost(self) -> float:
        """
        get the optimal cost of reaching the goal corresponding to the found optimal path.
        :return: the found optimal cost value
        """
        return not NotImplemented

    @abstractmethod
    def get_optimal_path(self) -> List[SearchState]:
        """
        get the optimal path found during the search, corresponding to the found optimal cost value.
        :return:
        """
        return NotImplemented




