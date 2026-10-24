import networkx as nx
from algorithms.augmentPathImpl import augmentPath
from typing import Any
from .residualGraph import buildResidualGraph


def augmentPathBFS(graph: nx.DiGraph, s) -> dict[Any,tuple[Any, float]]:
    nodeLabels = { node: (None, float('inf')) for node in graph.nodes}
    nodeLabels[s] = (s, float('inf'))
    visited: set[Any] = {s}
    queue = [s]

    while len(queue) > 0:
        #retrieving node from queue
        node = queue.pop(0)
        pred, currNode_flow = nodeLabels[node]
        #checking if connected nodes already have a label
        for u, v, data in graph.out_edges(node, data=True):
            #discarding nodes already visited with label
            if v in visited:
                continue
            if data["capacity"] == data["flow"]:
                continue
            new_flow = 0
            #calculating flow value towards v, capacity- flow works for both direct and reverse edges
            new_flow = min(currNode_flow, data["capacity"])
            #updating label for v
            nodeLabels[v] = (node, new_flow)
            #label set for v, therefore already visited
            visited.add(v)
            queue.append(v)
            
    return nodeLabels

"""
Calculates maximum flow from s to t and returns flow graph with flow and capacity for each edge
Return graph also has reverse edges with isResidualEdge property set to True
"""
def maxFlow(graph: nx.DiGraph, s, t) -> tuple[int, nx.DiGraph]:
    #creating a copy of the graph and preparing it for maxFlow algorithm
    workingGraph = graph.copy()

    for u, v in workingGraph.edges:
        if "flow" not in workingGraph[u][v]:
            workingGraph[u][v]["flow"] = 0
        if "capacity" not in workingGraph[u][v]:
            workingGraph[u][v]["capacity"] = 0

    optimalState = False


    while not optimalState:
        R = buildResidualGraph(workingGraph)
        #find augmenting path towards every other node with BFS visit
        nodeLabels = augmentPathBFS(R,s)

        #first predecessor and bottleneck value (the flow gain in this iteration)
        firstPred, augmFlow = nodeLabels[t]
        #no new augmenting path found, algorithm stops for optimality condition
        if firstPred is None:
            optimalState = True
            continue

        #reversely crossing the augmenting path
        nodePath = []
        current = t
        pred = None
        while True:
            nodePath.append(current)
            pred, flow = nodeLabels[current]
            if current == pred:
                break
            current = pred

        nodePath.reverse()
        edges_path: list[tuple[Any,Any, bool]] = [(nodePath[i],nodePath[i+1], R[nodePath[i]][nodePath[i+1]].get("isReverseEdge",False)) for i in range(len(nodePath)-1)]
        workingGraph = augmentPath(workingGraph,edges_path,int(augmFlow))
    #max flow equals to the sum of flow into t, the sink
    maxFlowValue = 0
    for u,v,data in workingGraph.in_edges(t, data= True):
        maxFlowValue+= data["flow"]

    return maxFlowValue, workingGraph
    