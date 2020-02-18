from functools import partial
from operator import itemgetter
from typing import Iterable, Tuple, List, Set

import networkx as nx

from experiments.vertex_cover import show_state, get_cover, generate_vc_problem_graph
from experiments.vertex_cover.vertex_cover_utils import bisect_contains
from hesearch.algorithms.search import AbstractHeuristic
from hesearch.framework.problem import SearchState, SearchSpace


def validate_order(it: Iterable):
    it = iter(it)
    try:
        first = next(it)
        while True:
            try:
                second = next(it)
                assert(first < second)
                first = second

            except StopIteration:
                break

    except StopIteration:
        pass


class VertexCoverState(SearchState):
    def __init__(self, graph: nx.Graph, vertices: Tuple[int]):
        self.graph = graph
        self.vertices = vertices
        validate_order(vertices)
        self.state_id = ",".join(map(str, self.vertices))

    def get_id(self) -> str:
        return self.state_id

    def get_cover(self) -> List[Tuple[int, int]]:
        return get_cover(self.graph, self.vertices)

    def display(self):
        show_state(self.graph, self.vertices)


class VertexCoverProblem(SearchSpace):

    def __init__(self, size: int = 30, difficulty: float = 0.5, seed: int = None):
        self.graph: nx.Graph = None
        self.regenerate_problem(size, difficulty, seed)

    def regenerate_problem(self, size: int = 30, difficulty: float = 0.5, seed: int = None):
        self.graph = generate_vc_problem_graph(size, difficulty, seed)

    def get_initial_state(self) -> VertexCoverState:
        return VertexCoverState(self.graph, tuple())

    def generate_children(self, state: VertexCoverState) -> Iterable[Tuple[VertexCoverState, float]]:
        state_max_vertex = max(state.vertices) if state.vertices else -1
        residual_vertices = self.__get_residual_vertices(state.vertices)
        for v in residual_vertices:
            if v > state_max_vertex:
                yield VertexCoverState(self.graph, state.vertices + (v,)), 1

    def __get_residual_vertices(self, vertices: Tuple[int]):
        residual = [n for n in self.graph.nodes if not bisect_contains(vertices, n)]
        return residual

    def is_goal(self, state: VertexCoverState) -> bool:
        num_covered_edges = len(state.get_cover())
        num_not_covered = self.graph.number_of_edges() - num_covered_edges
        return num_not_covered == 0


class VertexCoverHeuristic(AbstractHeuristic):
    def __init__(self, vc_problem: VertexCoverProblem):
        self.vc_problem = vc_problem

        self.min_value = float('inf')

    @property
    def graph(self) -> nx.Graph:
        return self.vc_problem.graph

    def __call__(self, state: VertexCoverState) -> int:
        return self.estimate(state)

    def estimate(self, state: VertexCoverState) -> int:
        covered_edges = set(state.get_cover())
        calc_res_degree = partial(self.__residual_degree, covered_edges=covered_edges)

        residual_vertices = [n for n in self.graph.nodes() if n not in state.vertices]
        # residual_degrees = sorted(map(calc_res_degree, residual_vertices), reverse=True)


        residual_vertices = sorted(zip(residual_vertices, map(calc_res_degree, residual_vertices)), key=itemgetter(1), reverse=True)
        h_vertices = set()
        h = 0
        num_not_covered = self.graph.number_of_edges() - len(covered_edges)
        for v, d in residual_vertices:
            for n in self.graph.neighbors(v):
                if n in h_vertices:
                    d -= 1
                    break

            h_vertices.add(v)
            h += 1
            num_not_covered -= d
            if num_not_covered <= 0:
                break

        if h < self.min_value:
            self.min_value = h
            print(h)
        return h

    def __residual_degree(self, v: int, covered_edges: Set[Tuple[int, int]]):
        residual_dgeree = 0
        for u in self.graph.neighbors(v):
            if (v, u) not in covered_edges and (u, v) not in covered_edges:
                residual_dgeree += 1

        return residual_dgeree





