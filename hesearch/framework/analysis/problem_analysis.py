from typing import Iterable, Tuple

from hesearch.framework.problem import SearchSpace, SearchState


class SearchSpaceAnalysisWrapper(SearchSpace):

    def __init__(self, problem: SearchSpace):
        self.problem = problem

        self.data_file = None

        self.nodes_generated = 0
        self.goals_found = 0
        self.duplicate_nodes_generated = 0
        self.avg_generation_time = None
        self.max_generation_time = None
        self.min_generation_time = None
        self.num_steps = 0

    def generate_children(self, state: SearchState) -> Iterable[Tuple[SearchState, float]]:
        pass

    def is_goal(self, state: SearchState) -> bool:
        pass

    def get_initial_state(self) -> SearchState:
        pass


