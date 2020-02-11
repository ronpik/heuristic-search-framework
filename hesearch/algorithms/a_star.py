from hesearch.algorithms.search.abc_heuristic import AbstractHeuristic
from hesearch.framework.problem import SearchSpace


class AStarBFS(object):
    def __init__(self, problem: SearchSpace, heuristic: AbstractHeuristic):
        self.problem = problem
        self.heuristic = heuristic

    def search(self):
        open = set()
        closed = set()

        s = self.problem.get_initial_state()

