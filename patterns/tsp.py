import math

from ortools.constraint_solver import routing_enums_pb2, pywrapcp


# documentation: https://developers.google.com/optimization/routing/tsp
def tsp(coords, time_limit=1):
    manager = pywrapcp.RoutingIndexManager(len(coords), 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    dmatrix = distance_matrix(coords)

    routing.SetArcCostEvaluatorOfAllVehicles(
        routing.RegisterTransitCallback(
            lambda from_index, to_index: dmatrix[manager.IndexToNode(from_index)][
                manager.IndexToNode(to_index)
            ]
        )
    )

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = time_limit

    solution = routing.SolveWithParameters(search_parameters)

    solution_coords = []

    index = routing.Start(0)
    while not routing.IsEnd(index):
        solution_coords.append(coords[manager.IndexToNode(index)])
        index = solution.Value(routing.NextVar(index))

    return solution_coords


def distance_matrix(coords):
    matrix = {}
    for from_index, from_node in enumerate(coords):
        matrix[from_index] = {}
        for to_index, to_node in enumerate(coords):
            if from_index == to_index:
                matrix[from_index][to_index] = 0
            else:
                matrix[from_index][to_index] = int(
                    math.sqrt(
                        (from_node[0] - to_node[0]) ** 2
                        + (from_node[1] - to_node[1]) ** 2
                    )
                )
    return matrix
