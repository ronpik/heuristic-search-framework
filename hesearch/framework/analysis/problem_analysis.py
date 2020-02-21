import json
from collections import Counter
from itertools import groupby
from operator import itemgetter
from typing import Iterable, Tuple

from hesearch.framework.problem import SearchSpace, SearchState


class SearchSpaceAnalysisWrapper(SearchSpace):

    def __init__(self, search_space: SearchSpace):
        self.search_space = search_space

        self.data_file = None

        self.nodes_counts = Counter()

        self.nodes_generated = 0
        self.goals_found = 0
        self.duplicate_nodes_generated = 0
        self.avg_generation_time = None
        self.max_generation_time = None
        self.min_generation_time = None
        self.num_steps = 0

        # TODO measure time

    def generate_children(self, state: SearchState) -> Iterable[Tuple[SearchState, float]]:
        children = self.search_space.generate_children(state)
        for c, cost in children:
            child_id = c.get_id()
            self.nodes_counts[child_id] += 1
            yield c, cost

    def is_goal(self, state: SearchState) -> bool:
        is_goal_answer = self.search_space.is_goal(state)
        if is_goal_answer:
            self.goals_found += 1

        return is_goal_answer

    def get_initial_state(self) -> SearchState:
        return self.search_space.get_initial_state()

    def show_analysis(self):
        print(f"number of times goal was generated: {self.goals_found}")
        for num_generated, nodes in groupby(self.nodes_counts.most_common(), key=itemgetter(1)):
            nodes = list(nodes)
            print(f"{len(nodes)} nodes have been generated {num_generated} times: {nodes}")

        total_generated = sum(self.nodes_counts.values())
        print(f"total nodes generated: {total_generated}")


