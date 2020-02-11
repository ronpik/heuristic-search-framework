from operator import itemgetter

from hesearch.algorithms import UniformCostSearch
from hesearch.experiments.real_distance_pathfinder import RealDistanceGraphProblem, RealDistanceHeuristic

if __name__ == "__main__":
    problem = RealDistanceGraphProblem(size=100, seed=71070)
    ucs_solver = UniformCostSearch()
    ucs_solver.set_search_space(problem)
    ucs_solver.search()
    cost = ucs_solver.get_optimal_cost()
    optimal_path = ucs_solver.get_optimal_path()

    print(cost)
    optimal_path = [node.get_id() for node in optimal_path]
    print(" -> ".join(map(str, optimal_path)))
    problem.show_solution(optimal_path)


    # heuristic = RealDistanceHeuristic(problem)
