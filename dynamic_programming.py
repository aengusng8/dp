import itertools
import matplotlib.pyplot as plt
from util import (
    City,
    read_cities,
    write_cities_and_return_them,
    generate_cities,
    path_cost,
    visualize_tsp,
)


def create_sets(size, n_vertices):
    sets = []
    for C in itertools.combinations(range(1, n_vertices), size):
        sets.append(frozenset(C) | {0})  # add 0 to the set
    return sets


def initialize_smallest_subproblems(distance_matrix):
    # If size of S is 2, then S must be {0, i}, and C(S, i) = dist(1, i)
    subproblems = {}
    for idx, dist in enumerate(distance_matrix[0][1:]):
        subproblems[(frozenset([0, idx + 1]), idx + 1)] = (dist, [0, idx + 1])
    return subproblems


def compute_min_distance(_set, i, subproblems, distance_matrix):
    # computes the minimum distance for each subset using previously solved subproblems
    # NOTE: Let us define a term C(S, i) be the cost of the minimum cost path visiting each vertex in set S exactly once,
    # starting at 0 and ending at i.
    # NOTE: C(S, i) = min {C(S-{i}, k) + dis(k, i)} where k belongs to S, k != i and k != 1.
    # k is the last vertex in the path before i
    optimal_result = min(
        [
            (
                subproblems[(_set - {i}, k)][0] + distance_matrix[k][i],  # distance
                subproblems[(_set - {i}, k)][1] + [i],  # path
            )
            for k in _set
            if k != 0 and k != i
        ]
    )

    return optimal_result


def solve_tsp_dynamic(vertices):
    n_vertices = len(vertices)
    # compute the distance matrix between all pairs of vertices.
    distance_matrix = [[x.distance(y) for y in vertices] for x in vertices]
    # initializes a dictionary subproblems that will store the optimal solutions for all subproblems of size 1
    subproblems = initialize_smallest_subproblems(distance_matrix)
    print("subproblems", subproblems)

    #     subproblems = {
    #     (frozenset({0, 1}), 1): (5.882329470541408, [0, 1]),
    #     (frozenset({0, 2}), 2): (5.421475813835195, [0, 2]),
    # ...
    #     (frozenset({0, 15}), 15): (1.412090648648308, [0, 15]),
    # }

    # NOTE: The loop that follows iteratively solves subproblems of increasing size.
    # loop over all sizes (subproblems to bigger subproblems = lower levels to higher levels in the tree)
    for size in range(2, n_vertices):
        bigger_subproblems = {}
        # Generate all possible subsets of size m that include city 0
        sets = create_sets(size, n_vertices)

        # loop over all sets with the same size: a level in the tree
        for _set in sets:
            for i in _set - {0}: # i is the last city visited
                # NOTE: Let us define a term C(S, i) be the cost of the minimum cost path visiting each vertex in set S exactly once,
                # starting at 1 and ending at i.
                # NOTE: C(S, i) = min { C(S-{i}, k) + dis(k, i)} where k belongs to S, k != i and k != 1.
                bigger_subproblems[(_set, i)] = compute_min_distance(
                    _set, i, subproblems, distance_matrix
                )
                # print("_set", _set, "i", i)
                # print("bigger_subproblems", bigger_subproblems)
                # raise

        # Update the subproblems
        subproblems = bigger_subproblems

    print("subproblems", subproblems)
    # Find the minimum total distance by adding the distance from the city 0 to the last city visited
    res = min(
        [
            (
                subproblems[d][0] + distance_matrix[0][d[1]],
                subproblems[d][1],
            )  # d[1] is the last city visited
            for d in iter(subproblems)
        ]
    )
    return res[1]


if __name__ == "__main__":
    vertices = read_cities(8)
    ind_shortest_path = solve_tsp_dynamic(vertices)
    vertices_shortest_path = [vertices[i] for i in ind_shortest_path]

    print("Shortest path :", *ind_shortest_path, sep=" -> ")
    print("Minimum path cost :", path_cost(vertices_shortest_path))
    visualize_tsp(
        "Travelling Salesman Problem: Dynamic Programming", vertices_shortest_path
    )
