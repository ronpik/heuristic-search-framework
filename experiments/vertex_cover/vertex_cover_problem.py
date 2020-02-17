from functools import partial
from typing import Iterable, Tuple, List, Set

import networkx as nx

from experiments.vertex_cover import show_state, get_cover, generate_vc_problem_graph
from hesearch.algorithms.search import AbstractHeuristic
from hesearch.framework.problem import SearchState, SearchSpace


class VertexCoverState(SearchState):
    def __init__(self, graph: nx.Graph, vertices: Iterable[int]):
        self.graph = graph
        self.vertices = set(vertices)
        self.state_id = ",".join(map(str, sorted(self.vertices)))

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
        return VertexCoverState(self.graph, [])

    def generate_children(self, state: VertexCoverState) -> Iterable[Tuple[VertexCoverState, float]]:
        residual_vertices = self.__get_residual_vertices(state.vertices)
        for v in residual_vertices:
            yield VertexCoverState(self.graph, state.vertices.union([v])), 1

    def __get_residual_vertices(self, vertices: Set[int]):
        residual = [n for n in self.graph.nodes if n not in vertices]
        return residual

    def is_goal(self, state: VertexCoverState) -> bool:
        num_covered_edges = len(state.get_cover())
        num_not_covered = self.graph.number_of_edges() - num_covered_edges
        return num_not_covered == 0


class VertexCoverHeuristic(AbstractHeuristic):
    def __init__(self, vc_problem: VertexCoverProblem):
        self.vc_problem = vc_problem

    @property
    def graph(self) -> nx.Graph:
        return self.vc_problem.graph

    def __call__(self, state: VertexCoverState) -> int:
        return self.estimate(state)

    def estimate(self, state: VertexCoverState) -> int:
        covered_edges = set(state.get_cover())
        calc_res_degree = partial(self.__residual_degree, covered_edges=covered_edges)

        residual_vertices = [n for n in self.graph.nodes() if n not in state.vertices]
        residual_degrees = sorted(map(calc_res_degree, residual_vertices), reverse=True)

        h = 0
        num_not_covered = self.graph.number_of_edges() - len(covered_edges)
        for d in residual_degrees:
            h += 1
            num_not_covered -= d
            if num_not_covered <= 0:
                break

        return h

    def __residual_degree(self, v: int, covered_edges: Set[Tuple[int, int]]):
        residual_dgeree = 0
        for u in self.graph.neighbors(v):
            if (v, u) not in covered_edges and (u, v) not in covered_edges:
                residual_dgeree += 1

        return residual_dgeree





