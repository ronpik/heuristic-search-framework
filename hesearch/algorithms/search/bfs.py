import heapq
from abc import ABC
from operator import itemgetter
from typing import List, NamedTuple

from hesearch.algorithms.search.abc_heuristic import CostSearcher, StateContext
from hesearch.framework.problem import SearchState, SearchSpace


ROOT_REACH_COST = 0.0


class OpenNode(NamedTuple):
    node_cost: float
    node: SearchState
    parent: SearchState
    node_reaching_cost: float
    depth: int


class BaseBFS(CostSearcher, ABC):

    def __init__(self):
        self.search_space: SearchSpace = None
        self.openlist: list = None
        self.num_open = 0
        self.closed: set = None
        self.parents: dict = None
        self.reaching_costs: dict = None

        self.goal: SearchState = None
        self.goal_cost: float = -1

    def set_search_space(self, search_space: SearchSpace):
        self.search_space = search_space

    def search(self):
        root = self.search_space.get_initial_state()
        root_context = StateContext(root, depth=0, reaching_cost=ROOT_REACH_COST)
        s_cost = self.evaluate_cost(root_context)
        root = OpenNode(node_cost=s_cost, node=root, parent=None, node_reaching_cost=ROOT_REACH_COST, depth=0)
        self.openlist = iter([root])
        self.num_open += 1
        self.parents = {}
        self.closed = set()

        while self.num_open > 0:
            best = next(self.openlist)
            self.num_open -= 1
            best_id = best.node.get_id()

            # the cost at the first time a node is chosen for expansion, is the the lowest cost
            # and the path corresponding to this cost is the optimal path to this node
            self.parents[best_id] = best.parent

            if self.search_space.is_goal(best.node):
                self.goal = best.node
                self.goal_cost = best.node_cost
                return

            if best_id in self.closed:
                continue

            # avoiding self loops (when the child of a node is the node itself
            self.closed.add(best_id)
            children_depth = best.depth + 1
            children_data = []
            for child, relative_cost in self.search_space.generate_children(best.node):
                child_id = child.get_id()
                if child_id in self.closed:
                    continue

                child_reaching_cost = best.node_reaching_cost + relative_cost
                child_context = StateContext(child, children_depth, child_reaching_cost)
                child_total_cost = self.evaluate_cost(child_context)
                open_child = OpenNode(node_cost=child_total_cost, node=child, parent=best.node, node_reaching_cost=child_reaching_cost, depth=children_depth)
                children_data.append(open_child)

            self.openlist = iter(list(heapq.merge(self.openlist, children_data, key=itemgetter(0))))
            self.num_open += len(children_data)

    def get_optimal_cost(self) -> float:
        return self.goal_cost

    def get_optimal_path(self) -> List[SearchState]:
        path = [self.goal]
        parent = self.parents[self.goal.get_id()]
        while parent is not None:
            path.append(parent)
            parent = self.parents[parent.get_id()]

        return list(reversed(path))
