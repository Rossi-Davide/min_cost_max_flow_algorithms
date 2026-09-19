import networkx as nx
from typing import Any

def bellmanFordNegativeCycleDetection(graph: nx.DiGraph) -> list[tuple[Any,int]]:

    nodeLabels: dict[Any, tuple[Any | None, int]] = {
        node: (None, 0) for node in graph.nodes
    }

    for _ in range(graph.number_of_nodes() - 1):
        for u, v in graph.edges:
            if nodeLabels[u][1] + graph[u][v]["cost"] < nodeLabels[v][1]:
                nodeLabels[v] = (u,nodeLabels[u][1] + graph[u][v]["cost"])

    vertex = None

    for u, v in graph.edges:
        if nodeLabels[u][1] + graph[u][v]["cost"] < nodeLabels[v][1]:
            nodeLabels[v] = (u,nodeLabels[u][1] + graph[u][v]["cost"])
            vertex = v

    if vertex is None:
        return []


    negativeLoop:list[tuple[Any,int]] = [(vertex,nodeLabels[vertex][1])]

    currNode = nodeLabels[vertex][0]
    while currNode != vertex:
        pred, cost = nodeLabels[currNode]
        negativeLoop.append((currNode,cost))
        currNode = pred

    return negativeLoop
    