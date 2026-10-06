import networkx as nx
from typing import Any
"""
Builds a residual graph by adding reverse edges 
and eliminating edges with saturated flow
Each edge has properties: flow,capacity,isResidualEdge
"""
def buildResidualGraph(graph: nx.DiGraph) -> nx.DiGraph:

    R = graph.copy()

    #setting flow and capacity for each edge
    for u, v in R.edges:
        if "flow" not in R[u][v]:
            R[u][v]["flow"] = 0
        if "capacity" not in R[u][v]:
            R[u][v]["capacity"] = 0


    #creating reverse edges if non existent
    for u,v in R.edges:
        if (not R.has_edge(v, u)) and R[u][v]["flow"] > 0:
            R.add_edge(v, u, capacity=0, flow= -R[u][v]["flow"], isResidualEdge = True)
            if R[u][v].get("cost", False):
                R[v][u]["cost"] = -R[u][v]["cost"]

    #removing saturated edges
    toDelete: list[tuple[Any,Any]] = []

    for u,v in R.edges:
        if R[u][v]["flow"] == R[u][v]["capacity"]:
            toDelete.append((u,v))

    for u,v in toDelete:
        R.remove_edge(u,v)
        
    return R