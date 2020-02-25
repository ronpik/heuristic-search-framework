import random

from experiments.n_puzzle.npuzzle_problem import NPuzzleProblem, NPuzzleManhattanDistanceHeuristicEstimator
from hesearch.algorithms import AStar, IDAStar

from hesearch.framework.analysis import SearchSpaceAnalysisWrapper, HeuristicBFSCostSearchAnalyzer, \
    HeuristicIDCostSearchAnalyzer

if __name__ == "__main__":

    n = 4
    random_seed = 71070
    max_permutation_steps = 150

    # r = random.Random(random_seed)
    permutation_steps = random.randint(0, max_permutation_steps)
    print(f"permutaion_steps: {permutation_steps}")

    search_algos = []
    # search_algos.append(UniformCostSearch())
    # search_algos.append(IDDFS())

    problem = NPuzzleProblem(n, seed=random_seed, optimal_depth=permutation_steps)
    heuristic = NPuzzleManhattanDistanceHeuristicEstimator(n)
    astar = AStar(heuristic)
    astar = HeuristicBFSCostSearchAnalyzer(astar, "./analysis-results/n_puzzle-astar")
    # search_algos.append(astar)

    ida_star = IDAStar(heuristic)
    ida_star = HeuristicIDCostSearchAnalyzer(ida_star, f"./analysis-results/4_puzzle-ida_star-{permutation_steps}_steps")
    search_algos.append(ida_star)

    for solver in search_algos:

        # initialize search space
        problem = NPuzzleProblem(n, seed=random_seed, optimal_depth=permutation_steps)
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