from experiments.n_puzzle.npuzzle_problem import NPuzzleProblem, NPuzzleManhattanDistanceHeuristicEstimator
from hesearch.algorithms import UniformCostSearch, AStar, IDAStar
from hesearch.algorithms.impl_bfs import HeuristicBFSCostSearchAnalyzer, HeuristicIDCostSearchAnalyzer
from hesearch.framework.analysis.problem_analysis import SearchSpaceAnalysisWrapper

if __name__ == "__main__":

    n = 4
    random_seed = 71070
    optimal_steps = 50

    search_algos = []
    # search_algos.append(UniformCostSearch())
    # search_algos.append(IDDFS())

    problem = NPuzzleProblem(n, seed=random_seed, optimal_depth=optimal_steps)
    heuristic = NPuzzleManhattanDistanceHeuristicEstimator(n)
    astar = AStar(heuristic)
    astar = HeuristicBFSCostSearchAnalyzer(astar, "n_puzzle-astar")
    search_algos.append(astar)

    ida_star = IDAStar(heuristic)
    ida_star = HeuristicIDCostSearchAnalyzer(ida_star, "4_puzzle-ida_star")
    search_algos.append(ida_star)

    for solver in search_algos:

        # initialize search space
        problem = NPuzzleProblem(n, seed=random_seed, optimal_depth=optimal_steps)
        problem_analyzer = SearchSpaceAnalysisWrapper(problem)

        print(f"\nSearch optimal path using {solver.__class__}")
        solver.set_search_space(problem_analyzer)
        solver.search()
        cost = solver.get_optimal_cost()
        optimal_path = solver.get_optimal_path()

        # display some info
        print(cost)
        for s in optimal_path:
            print(s.display())
            print()

        problem_analyzer.show_analysis()