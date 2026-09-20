import networkx as nx
from typing import Any

def augmentPath(graph:nx.DiGraph, nodes: list[Any], augmFlow: int) -> nx.DiGraph:

    edges: list[tuple[Any,Any]] = [(nodes[i],nodes[i+1]) for i in range(len(nodes)-1)]
    edges.append((nodes[len(nodes)-1],nodes[0]))

    for u,v in edges:
        graph.edges[u,v]["flow"] = graph.edges[u,v]["flow"] + augmFlow
        
        #creating reverse edge if non existent
        if not graph.has_edge(v, u):
            graph.add_edge(v, u, capacity=0, flow=0, isResidualEdge = True)

        #updating flow on reverse edge
        graph.edges[v, u]["flow"] = graph.edges[v, u]["flow"] - augmFlow

    return graph