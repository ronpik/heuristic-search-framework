from math import sqrt
from operator import itemgetter
from typing import Tuple, List

import networkx as nx
from matplotlib import pyplot as plt

DEFAULT_SEED = 71070
DEFAULT_SIZE = 100


def generate_waxman_graph(size: int = DEFAULT_SIZE, seed: int = None) -> nx.Graph:
    if seed is None:
        seed = DEFAULT_SEED

    g = nx.waxman_graph(size, seed=seed)
    cc = nx.connected_components(g)
    giant_component_nodes = max(cc, key=len)
    g = g.subgraph(giant_component_nodes).copy()
    return g


def euclidian_distance(x: float, y: float) -> float:
    return sqrt((x ** 2) + (y ** 2))


def get_endpoints_nodes(g: nx.waxman_graph) -> Tuple[int, int]:
    source, goal = None, None
    min_dist = float('inf')
    max_dist = -1
    for node, attrs in g._node.items():
        pos = attrs["pos"]
        dist = euclidian_distance(*pos)
        if dist < min_dist:
            min_dist = dist
            source = node

        if dist > max_dist:
            max_dist = dist
            goal = node

    print(source, goal)
    return source, goal


def generate_real_distance_graph_problem(size: int, seed: int = None) -> Tuple[nx.Graph, int, int]:
    g = generate_waxman_graph(size, seed)
    s, t = get_endpoints_nodes(g)
    show_waxman_graph(g, s, t)
    return g, s, t


def show_waxman_graph(waxman_graph: nx.Graph, source: int = None, goal: int = None, path: List[int] = None):
    pos = {n: attrs["pos"] for n, attrs in waxman_graph._node.items()}
    nodeslist = list(waxman_graph.nodes)
    nodes_colors = ["b"] * len(nodeslist)

    edgeslist = list(waxman_graph.edges())
    edge_colors = ["black"] * len(edgeslist)

    if source is not None:
        source_index = nodeslist.index(source)
        nodes_colors[source_index] = 'r'

    if goal is not None:
        goal_index = nodeslist.index(goal)
        nodes_colors[goal_index] = 'g'

    if path is not None:
        for i in range(len(path) - 1):
            edge = tuple(path[i: i + 2])
            edge_index = None
            try:
                edge_index = edgeslist.index(edge)
            except ValueError:
                u, v = edge
                edge_index = edgeslist.index((v, u))

            edge_colors[edge_index] = 'r'

    nx.draw_networkx(waxman_graph, pos, nodelist=nodeslist, node_color=nodes_colors, edge_color=edge_colors)
    plt.show()


if __name__ == "__main__":
    g = generate_waxman_graph()
    s, t = get_endpoints_nodes(g)
    show_waxman_graph(g, source=s, goal=t)
