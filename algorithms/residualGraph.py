import networkx as nx
from typing import Any
"""
Builds a residual graph by adding reverse edges 
and eliminating edges with saturated flow
Each edge has properties: flow,capacity,isResidualEdge
"""
def buildResidualGraph(graph: nx.DiGraph) -> nx.DiGraph:

    R = nx.DiGraph()
    for node in graph.nodes:
        R.add_node(node)
        if 'x' in graph.nodes[node]:
            R.nodes[node]['x'] = graph.nodes[node]['x']
        if 'e' in graph.nodes[node]:
            R.nodes[node]['e'] = graph.nodes[node]['e']
        if 'potential' in graph.nodes[node]:
            R.nodes[node]['potential'] = graph.nodes[node]['potential']
    R.add_nodes_from(graph.nodes)

    #setting flow and capacity for each edge
    for u, v in graph.edges:
        if graph[u][v]["capacity"] - graph[u][v]["flow"] > 0:
            R.add_edge(u,v,capacity=graph[u][v]["capacity"] - graph[u][v]["flow"], flow=0)
        if graph[u][v]["flow"] > 0:
            R.add_edge(v,u,capacity=0,flow=-graph[u][v]["flow"], isReverseEdge=True)
        if graph[u][v].get("cost", -1) >= 0:
            if R.has_edge(u,v):
                R[u][v]["cost"] = graph[u][v]["cost"]
            if R.has_edge(v,u):
                R[v][u]["cost"] = -graph[u][v]["cost"]
    return R