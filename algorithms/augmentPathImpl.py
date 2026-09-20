import networkx as nx
from typing import Any

def augmentPath(graph:nx.DiGraph, edges: list[tuple[Any,Any]], augmFlow: int) -> nx.DiGraph:

    for u,v in edges:
        graph.edges[u,v]["flow"] = graph.edges[u,v]["flow"] + augmFlow
        
        #creating reverse edge if non existent
        if not graph.has_edge(v, u):
            graph.add_edge(v, u, capacity=0, flow=0, isResidualEdge = True)

        #updating flow on reverse edge
        graph.edges[v, u]["flow"] = graph.edges[v, u]["flow"] - augmFlow

    return graph