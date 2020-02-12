from operator import itemgetter

from hesearch.algorithms import UniformCostSearch
from hesearch.algorithms.impl_bfs import AStar, IDDFS, IDAStar
from hesearch.experiments.real_distance_pathfinder import RealDistanceGraphProblem, RealDistanceHeuristic
from hesearch.framework.analysis.problem_analysis import SearchSpaceAnalysisWrapper

if __name__ == "__main__":

    problem_size = 100
    random_seed = 71070

    search_algos = []
    search_algos.append(UniformCostSearch())
    # search_algos.append(IDDFS())

    problem = RealDistanceGraphProblem(size=problem_size, seed=random_seed)
    heuristic = RealDistanceHeuristic(problem)
    search_algos.append(AStar(heuristic))
    search_algos.append(IDAStar(heuristic))

    for solver in search_algos:

        # initialize search space
        problem = RealDistanceGraphProblem(size=problem_size, seed=random_seed)
        problem_analyzer = SearchSpaceAnalysisWrapper(problem)

        print(f"\nSearch optimal path using {solver.__class__}")
        solver.set_search_space(problem_analyzer)
        solver.search()
        cost = solver.get_optimal_cost()
        optimal_path = solver.get_optimal_path()

        # display some info
        print(cost)
        optimal_path = [node.get_id() for node in optimal_path]
        print(" -> ".join(map(str, optimal_path)))
        problem_analyzer.show_analysis()
        problem.show_solution(optimal_path)

        print()









