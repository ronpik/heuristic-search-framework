from hesearch.algorithms.search.abc_heuristic import StateContext


def uniform_cost(state_context: StateContext):
    return state_context.reaching_cost


def basic_heuristic_cost(g: float, h: float):
    return g + h

