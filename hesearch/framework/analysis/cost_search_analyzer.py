import csv
from abc import ABC
from typing import List, IO

from hesearch.algorithms.search.abc_heuristic import CostSearcher, StateContext, HeuristicEstimator, \
    HeuristicCostSearcher
from hesearch.algorithms.search.bfs import BaseBFS
from hesearch.framework.problem import SearchState, SearchSpace


class HeuristicCostSearchAnalyzer(HeuristicCostSearcher):

    INFO_HEADER = ["state_id", "depth", "g", "h", "f"]

    def __init__(self, cost_search_algo: HeuristicCostSearcher, name: str):
        self.searcher = cost_search_algo
        self.name = name
        self.__storage_f = self.__initialize_storage_file(name)
        self.__writer = csv.writer(self.__storage_f)

    @staticmethod
    def __initialize_storage_file(name: str) -> IO:
        f = open(f"{name}-hcs-analysis.csv", 'w')
        f.write(",".join(HeuristicCostSearchAnalyzer.INFO_HEADER))
        f.write("\n")
        return f

    def finalize(self):
        self.__storage_f.close()

    @property
    def heuristic(self) -> HeuristicEstimator:
        return self.searcher.heuristic

    def evaluate_heuristic_cost(self, state_context: StateContext, heuristic_value: float) -> float:
        f = self.searcher.evaluate_heuristic_cost(state_context, heuristic_value)
        self.__write_info(state_context, heuristic_value, f)
        return f

    def __write_info(self, state_context: StateContext, heuristic_value: float, total_cost_value: float):
        record = (state_context.state.get_id(), state_context.depth, state_context.reaching_cost, heuristic_value, total_cost_value)
        self.__writer.writerow(record)



