from bisect import bisect_left
from typing import Tuple, List, Set

import networkx as nx
from matplotlib import pyplot as plt


def generate_vc_problem_graph(size: int, difficulty: float = 0.5, seed: int = None) -> nx.Graph:
    """
    generates a random graph for solving the vertex-cover problem.
    :param size:
    :param edge_prob:
    :param seed:
    :return:
    """
    if difficulty < 0 or difficulty >= 1:
        raise ValueError("difficulty should be a non-negative value lower than 1: [0, 1)")

    edge_prob = 1 - difficulty
    g = nx.erdos_renyi_graph(size, edge_prob, seed=seed)
    cc = nx.connected_components(g)
    giant_component_nodes = max(cc, key=len)
    g = g.subgraph(giant_component_nodes).copy()
    return g


def get_cover(g: nx.Graph, vertices: Set[int]) -> List[Tuple[int, int]]:
    covered_edges = [e for e in g.edges() if e[0] in vertices or e[1] in vertices]
    return covered_edges


def bisect_contains(a, x):
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return True

    return False


def show_state(g: nx.Graph, vertices: Set[int]):

    vertices = set(vertices)
    chosen_vertices_color = ['r'] * len(vertices)

    covered_edges = get_cover(g, vertices)
    covered_edges_color = ['g'] * len(covered_edges)

    pos = nx.spring_layout(g, seed=1919)
    nx.draw_networkx(g, pos)
    nx.draw_networkx_nodes(g, pos, vertices, node_color=chosen_vertices_color)
    nx.draw_networkx_edges(g, pos, covered_edges, edge_color=covered_edges_color)
    plt.show()





