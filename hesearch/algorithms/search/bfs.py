import heapq
from abc import ABC
from typing import List

from hesearch.algorithms.search.abc_heuristic import AbstractCostSearch
from hesearch.framework.problem import SearchState, SearchSpace


class BaseBFS(AbstractCostSearch, ABC):

    def __init__(self):
        self.search_space: SearchSpace = None
        self.openlist: list = None
        self.closed: set = None
        self.parents: dict = None
        self.reaching_costs: dict = None

        self.goal: SearchState = None
        self.goal_cost: float = -1

    def set_search_space(self, search_space: SearchSpace):
        self.search_space = search_space

    def search(self):
        s = self.search_space.get_initial_state()
        self.openlist = [(0, s, None, 0)]
        self.parents = {}
        self.closed = set()

        while len(self.openlist) > 0:
            node_cost, node, parent, node_reaching_cost = heapq.heappop(self.openlist)
            node_id = node.get_id()

            # the cost at the first time a node is chosen for expansion, is the the lowest cost
            # and the path corresponding to this cost is the optimal path to this node
            self.parents[node_id] = parent

            if self.search_space.is_goal(node):
                self.goal = node
                self.goal_cost = node_cost
                return

            if node_id in self.closed:
                continue

            # avoiding self loops (when the child of a node is the node itself
            self.closed.add(node_id)

            for child, relative_cost in self.search_space.generate_children(node):
                child_id = child.get_id()
                if child_id in self.closed:
                    continue

                child_reaching_cost = node_reaching_cost + relative_cost
                child_total_cost = self.evaluate_cost(child, child_reaching_cost)
                heapq.heappush(self.openlist, (child_total_cost, child, node, child_reaching_cost))

    def get_optimal_cost(self) -> float:
        return self.goal_cost

    def get_optimal_path(self) -> List[SearchState]:
        path = [self.goal]
        parent = self.parents[self.goal.get_id()]
        while parent is not None:
            path.append(parent)
            parent = self.parents[parent.get_id()]

        return list(reversed(path))
