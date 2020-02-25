from hesearch.algorithms.search.abc_heuristic import HeuristicCostSearcher
from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.algorithms.search.iterative_deepening import BaseIterativeDeepening
from hesearch.framework.analysis.cost_search_analyzer import HeuristicCostSearchAnalyzer


class HeuristicBFSCostSearchAnalyzer(BaseBFS, HeuristicCostSearchAnalyzer):
    def __init__(self, cost_search_algo: HeuristicCostSearcher, name: str):
        BaseBFS.__init__(self)
        HeuristicCostSearchAnalyzer.__init__(self, cost_search_algo, name)


class HeuristicIDCostSearchAnalyzer(BaseIterativeDeepening, HeuristicCostSearchAnalyzer):

    def __init__(self, cost_search_algo: HeuristicCostSearcher, name: str):
        BaseIterativeDeepening.__init__(self)
        HeuristicCostSearchAnalyzer.__init__(self, cost_search_algo, name)

    def get_additional_header(self):
        return "bound",

    def get_additional_record(self) -> tuple:
        return self.bound,