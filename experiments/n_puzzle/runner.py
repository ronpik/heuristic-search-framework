from experiments.n_puzzle.npuzzle_problem import NPuzzleProblem, NPuzzleManhattanDistanceHeuristic
from hesearch.algorithms import UniformCostSearch, AStar, IDAStar
from hesearch.framework.analysis.problem_analysis import SearchSpaceAnalysisWrapper

if __name__ == "__main__":

    n = 5
    random_seed = 71070
    optimal_steps = 100

    search_algos = []
    # search_algos.append(UniformCostSearch())
    # search_algos.append(IDDFS())

    problem = NPuzzleProblem(n, seed=random_seed, optimal_depth=optimal_steps)
    heuristic = NPuzzleManhattanDistanceHeuristic(n)
    search_algos.append(AStar(heuristic))
    search_algos.append(IDAStar(heuristic))

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