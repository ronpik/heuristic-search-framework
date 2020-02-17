from typing import Iterable, Tuple
from abc import ABC, abstractmethod


class SearchState(ABC):

    @abstractmethod
    def get_id(self) -> str:
        return NotImplemented

    @abstractmethod
    def display(self) -> str:
        return repr(self)


class SearchSpace(ABC):

    @abstractmethod
    def generate_children(self, state: SearchState) -> Iterable[Tuple[SearchState, float]]:
        return NotImplemented

    @abstractmethod
    def is_goal(self, state: SearchState) -> bool:
        return NotImplemented

    @abstractmethod
    def get_initial_state(self) -> SearchState:
        return NotImplemented

