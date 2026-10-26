import networkx as nx
from typing import Any

def bellmanFordNegativeCycleDetection(graph: nx.DiGraph) -> list[Any]:

    #node: (predecessor, cost_to_reach_node)
    nodeLabels: dict[Any, tuple[Any | None, int]] = {
        node: (None, 0) for node in graph.nodes
    }

    for _ in range(graph.number_of_nodes() - 1):
        for u, v in graph.edges:
            if nodeLabels[u][1] + graph[u][v]["cost"] < nodeLabels[v][1]:
                nodeLabels[v] = (u,nodeLabels[u][1] + graph[u][v]["cost"])

    vertex = None

    # if relaxation happens again at nth iteration then there's a negative cycle
    for u, v in graph.edges:
        if nodeLabels[u][1] + graph[u][v]["cost"] < nodeLabels[v][1]:
            nodeLabels[v] = (u,nodeLabels[u][1] + graph[u][v]["cost"])
            vertex = v

    if vertex is None:
        return []

    #reverse path to reach source of loop
    for _ in range(graph.number_of_nodes()):
        pred, cost = nodeLabels[vertex]
        if pred is not None:
            vertex = pred

    #build negative loop nodes list
    negativeLoop:list[Any] = [vertex]

    currNode = nodeLabels[vertex][0]
    while currNode != vertex:
        pred, cost = nodeLabels[currNode]
        negativeLoop.append(currNode)
        currNode = pred

    negativeLoop.reverse()
    return negativeLoop
    