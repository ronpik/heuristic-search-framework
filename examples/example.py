from operator import itemgetter

from hesearch.algorithms import UniformCostSearch
from hesearch.algorithms.ucs import AStar
from hesearch.experiments.real_distance_pathfinder import RealDistanceGraphProblem, RealDistanceHeuristic
from hesearch.framework.analysis.problem_analysis import SearchSpaceAnalysisWrapper

if __name__ == "__main__":
    # initialize search space
    problem = RealDistanceGraphProblem(size=100, seed=71070)
    problem_analyzer = SearchSpaceAnalysisWrapper(problem)

    print("Search optimal path using Uniform Cost Search")
    # use uniform cost search algorithm
    ucs_solver = UniformCostSearch()
    ucs_solver.set_search_space(problem_analyzer)
    ucs_solver.search()
    cost = ucs_solver.get_optimal_cost()
    optimal_path = ucs_solver.get_optimal_path()

    # display some info
    print(cost)
    optimal_path = [node.get_id() for node in optimal_path]
    print(" -> ".join(map(str, optimal_path)))
    problem_analyzer.show_analysis()
    problem.show_solution(optimal_path)


    print("Search optimal path using A*")
    # initialize search space
    problem = RealDistanceGraphProblem(size=100, seed=71070)
    problem_analyzer = SearchSpaceAnalysisWrapper(problem)

    # use uniform cost search algorithm
    heuristic = RealDistanceHeuristic(problem)
    astar_solver = AStar(heuristic)
    astar_solver.set_search_space(problem_analyzer)
    astar_solver.search()
    cost = astar_solver.get_optimal_cost()
    optimal_path = astar_solver.get_optimal_path()

    # display some info
    print(cost)
    optimal_path = [node.get_id() for node in optimal_path]
    print(" -> ".join(map(str, optimal_path)))
    problem_analyzer.show_analysis()
    problem.show_solution(optimal_path)



