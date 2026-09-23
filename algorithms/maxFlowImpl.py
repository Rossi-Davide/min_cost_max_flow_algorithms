import networkx as nx
from augmentPathImpl import augmentPath
from typing import Any


def augmentPathBFS(graph: nx.DiGraph, s) -> dict[Any,tuple[int, int]]:
    nodeLabels = { node: (-1, -1) for node in graph.nodes}
    nodeLabels[s] = (s, -1)
    visited:set[int] = set(s)
    queue = [s]

    while len(queue) > 0:
        #retrieving node from queue
        index:int = queue.pop(0)
        pred, currNode_flow = nodeLabels[index]
        #checking connected nodes
        for u, v, data in graph.out_edges(index, data=True):
            #discarding nodes already visited with label
            if v in visited:
                continue
            if data["capacity"] - data["flow"]:
                continue
            new_flow = 0
            # s source case
            if currNode_flow < 0:
                new_flow = data["capacity"] - data["flow"]
            else:
                #calculating flow value towards v, capacity- flow works for both direct and reverse edges
                new_flow = min(currNode_flow, data["capacity"] - data["flow"])
            #updating label for v
            nodeLabels[v] = (index, new_flow)
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
        #find augmenting path towards every other node with BFS visit
        nodeLabels = augmentPathBFS(workingGraph,s)

        #first predecessor and bottleneck value (the flow gain in this iteration)
        firstPred, augmFlow = nodeLabels[t]
        #no new augmenting path found, algorithm stops for optimality condition
        if firstPred == -1:
            optimalState = True
            continue

        #reversely crossing the augmenting path and updating flow for each edge
        nodePath = [t]
        pred, flow = nodeLabels[t]
        endReverseTraversal = False
        while not endReverseTraversal:
            nodePath.append(pred)
            next_pred, flow = nodeLabels[pred]
            if pred == next_pred:
                endReverseTraversal = True
            pred = next_pred

        nodePath.reverse()
        workingGraph = augmentPath(workingGraph,nodePath,augmFlow)
    #max flow equals to the sum of flow into t, the sink
    maxFlowValue = 0
    for u,v,data in workingGraph.in_edges(t, data= True):
        if data["isResidualEdge"]:
            continue
        maxFlowValue+= data["flow"]

    return maxFlowValue, workingGraph
    