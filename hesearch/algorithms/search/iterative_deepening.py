from abc import ABC
from typing import List

from hesearch.algorithms.search.abc_heuristic import AbstractCostSearch
from hesearch.framework.problem import SearchState, SearchSpace

FOUND_FLAG = -1
ROOT_REACH_COST = 0
INFINITE_COST = float('inf')


# class AbstractDLS(ABC):


class BaseIterativeDeepening(AbstractCostSearch, ABC):

    def __init__(self, ):
        self.search_space: SearchSpace = None

        self.optimal_goal_cost: float = -1
        self.optimal_path: List[SearchState] = None

    def set_search_space(self, search_space: SearchSpace):
        self.search_space = search_space

    def search(self):
        root = self.search_space.get_initial_state()
        bound = self.evaluate_cost(root, ROOT_REACH_COST)
        path_stack = [root]

        while True:
            print(f"search with bound: {bound}")
            next_bound = self.search_dls(path_stack, ROOT_REACH_COST, bound)
            if next_bound == FOUND_FLAG:
                self.optimal_goal_cost = bound
                self.optimal_path = path_stack
                return

            if next_bound == INFINITE_COST:
                return None

            bound = next_bound

    def search_dls(self, path_stack: list, reaching_cost: float, bound: float) -> float:
        node = path_stack[-1]
        node_cost = self.evaluate_cost(node, reaching_cost)
        if node_cost > bound:
            return node_cost

        if self.search_space.is_goal(node):
            return FOUND_FLAG

        next_bound = INFINITE_COST
        for child, relative_cost in self.search_space.generate_children(node):
            if child not in path_stack:
                path_stack.append(child)
                child_reaching_cost = reaching_cost + relative_cost
                min_cost_exceeds = self.search_dls(path_stack, child_reaching_cost, bound)
                if min_cost_exceeds == FOUND_FLAG:
                    return FOUND_FLAG

                next_bound = min(next_bound, min_cost_exceeds)
                path_stack.pop()

        return next_bound

    def get_optimal_cost(self) -> float:
        return self.optimal_goal_cost

    def get_optimal_path(self) -> List[SearchState]:
        return self.optimal_path[:]
