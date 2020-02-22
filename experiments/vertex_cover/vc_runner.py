from experiments.vertex_cover import VertexCoverProblem, VertexCoverHeuristicEstimator
from hesearch.algorithms import UniformCostSearch, AStar, IDAStar
from hesearch.framework.analysis.problem_analysis import SearchSpaceAnalysisWrapper

if __name__ == "__main__":

    problem_size = 25
    random_seed = 71070

    search_algos = []
    # search_algos.append(UniformCostSearch())
    # search_algos.append(IDDFS())

    problem = VertexCoverProblem(size=problem_size, difficulty=0.9, seed=random_seed)
    heuristic = VertexCoverHeuristicEstimator(problem)
    search_algos.append(AStar(heuristic))
    search_algos.append(IDAStar(heuristic))

    for solver in search_algos:

        # initialize search space
        problem = VertexCoverProblem(size=problem_size, difficulty=0.9, seed=random_seed)
        problem_analyzer = SearchSpaceAnalysisWrapper(problem)

        print(f"\nSearch optimal path using {solver.__class__}")
        solver.set_search_space(problem_analyzer)
        solver.search()
        cost = solver.get_optimal_cost()
        optimal_path = solver.get_optimal_path()

        # display some info
        print(cost)
        optimal_solution = optimal_path[-1]
        optimal_vertices = optimal_solution.vertices
        print(optimal_vertices)

        problem_analyzer.show_analysis()

        optimal_solution.display()

        print()