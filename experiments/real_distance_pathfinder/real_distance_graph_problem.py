from math import sqrt
from typing import Iterable, Tuple, List

from hesearch.algorithms.search import HeuristicEstimator
from experiments.real_distance_pathfinder.real_distance_problem_generator import \
    generate_real_distance_graph_problem, show_waxman_graph
from hesearch.framework.problem import SearchSpace, SearchState

POSITION_FIELD = "pos"


def euclidean_distance(x1, y1, x2, y2):
    return sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


class RealDistanceNode(SearchState):

    def __init__(self, name: int, pos: Tuple[float, float]):
        self.name = name
        self.position = pos

    def __repr__(self):
        return repr((self.name, self.position))

    def get_id(self):
        return self.name

    def display(self) -> str:
        return repr(self)


class RealDistanceGraphProblem(SearchSpace):

    def __init__(self, size: int = 100, seed: int = None):
        graph, s, t = generate_real_distance_graph_problem(size, seed)
        self.graph = graph

        source_pos = graph._node[s][POSITION_FIELD]
        self.source = RealDistanceNode(s, source_pos)

        self.goal_pos = graph._node[t][POSITION_FIELD]
        self.goal = RealDistanceNode(t, self.goal_pos)

    def generate_children(self, state: RealDistanceNode) -> Iterable[Tuple[float, RealDistanceNode]]:
        node_name = state.name
        node_x, node_y = state.position
        neighbors = list(self.graph.neighbors(node_name))
        positions = [self.graph._node[n]['pos'] for n in neighbors]
        distances = [euclidean_distance(*pos, node_x, node_y) for pos in positions]
        children = list(zip(map(self.__to_state, neighbors), distances))
        return children

    def is_goal(self, state: RealDistanceNode) -> bool:
        return state.get_id() == self.goal.get_id()

    def get_initial_state(self) -> RealDistanceNode:
        return self.source

    def get_goal(self) -> RealDistanceNode:
        return self.goal

    def __to_state(self, name: int) -> RealDistanceNode:
        pos = self.graph._node[name][POSITION_FIELD]
        return RealDistanceNode(name, pos)

    def show_solution(self, optimal_path: List[int]):
        show_waxman_graph(self.graph, self.source.name, self.goal.name, optimal_path)


class RealDistanceHeuristicEstimator(HeuristicEstimator):
    def __init__(self, real_distance_problem: RealDistanceGraphProblem):
        self.goal_pos = real_distance_problem.get_goal().position
        self.goal_x, self.goal_y = self.goal_pos

    def estimate(self, state: RealDistanceNode) -> float:
        return self.__euclidean_distance(*state.position)

    def __euclidean_distance(self, x, y):
        return euclidean_distance(x, y, self.goal_x, self.goal_y)

    def __call__(self, state: RealDistanceNode) -> float:
        return self.estimate(state)

