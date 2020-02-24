import csv
from abc import ABC
from typing import List, IO

from hesearch.algorithms.search.abc_heuristic import StateContext, HeuristicEstimator, \
    HeuristicCostSearcher


EMPTY_RECORD = tuple()


class HeuristicCostSearchAnalyzer(HeuristicCostSearcher, ABC):

    BASE_HEADER = ("state_id", "depth", "g", "h", "f")

    def __init__(self, cost_search_algo: HeuristicCostSearcher, name: str):
        self.searcher = cost_search_algo
        self.name = name
        self.__storage_f = self.__initialize_storage_file(name)
        self.__writer = csv.writer(self.__storage_f)

    def __initialize_storage_file(self, name: str) -> IO:
        f = open(f"{name}-hcs-analysis.csv", 'w')
        header = self.__get_header()
        f.write(",".join(header))
        f.write("\n")
        return f

    def __get_header(self):
        base_header = self.BASE_HEADER
        add_header = self.get_additional_header()
        return base_header + add_header

    def get_additional_header(self):
        return EMPTY_RECORD

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
        record = self.__get_record(state_context, heuristic_value, total_cost_value)
        self.__writer.writerow(record)

    def __get_record(self, state_context: StateContext, heuristic_value: float, total_cost_value: float) -> tuple:
        base_record = (state_context.state.get_id(), state_context.depth, state_context.reaching_cost, heuristic_value, total_cost_value)
        add_record = self.get_additional_record()
        return base_record + add_record

    def get_additional_record(self) -> tuple:
        return EMPTY_RECORD






