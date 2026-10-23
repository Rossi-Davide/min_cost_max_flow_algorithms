import networkx as nx
from typing import Any

def augmentPath(graph:nx.DiGraph, edges: list[tuple[Any,Any,bool]], augmFlow: int) -> nx.DiGraph:

    for u,v, isResidualEdge in edges:
        if isResidualEdge:
            graph.edges[v,u]["flow"] = graph.edges[v,u]["flow"] - augmFlow
            if graph.edges[v,u]["flow"] < 0:
                raise ValueError("Flow value cannot go negative, error in the algorithm")
        else:
            graph.edges[u,v]["flow"] = graph.edges[v,u]["flow"] + augmFlow
            if graph.edges[u,v]["flow"] > graph.edges[u,v]["capacity"]:
                raise ValueError("Flow value cannot be above capacity, error in the algorithm")
    return graph