import heapq
from typing import Any, Dict

from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.framework.problem import SearchSpace, SearchState


class UniformCostSearch(BaseBFS):

    def evaluate_cost(self, state: SearchState, state_cost: float) -> float:
        return state_cost


# class UniformCostSearch(object):
#     def __init__(self, problem: SearchSpace):
#         self.problem = problem
#
#     def search(self):
#         s = self.problem.get_initial_state()
#         open_nodes = [(0, s)]
#         parents = {s.get_id(): None}
#         closed = set()
#
#         while len(open_nodes) > 0:
#             node_cost, node = heapq.heappop(open_nodes)
#             if self.problem.is_goal(node):
#                 optimal_path = self.__extract_path(node, parents)
#                 return node_cost, optimal_path
#
#             node_id = node.get_id()
#             if node_id in closed:
#                 continue
#
#             for child, cost in self.problem.generate_children(node):
#                 child_id = child.get_id()
#                 if child_id in closed:
#                     continue
#
#                 parents[child_id] = node
#                 child_total_cost = node_cost + cost
#                 heapq.heappush(open_nodes, (child_total_cost, child))
#                 closed.add(node_id)
#
#     @staticmethod
#     def __extract_path(node: SearchState, parents: Dict[Any, SearchState]):
#         path = [node]
#         parent = parents[node.get_id()]
#         while parent is not None:
#             path.append(parent)
#             parent = parents[parent.get_id()]
#
#         return list(reversed(path))



