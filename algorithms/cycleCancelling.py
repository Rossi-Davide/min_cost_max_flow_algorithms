import networkx as nx
from algorithms.bellmanFordNegativeCycleImpl import bellmanFordNegativeCycleDetection
from algorithms.maxFlowImpl import maxFlow 
from algorithms.augmentPathImpl import augmentPath
from algorithms.residualGraph import buildResidualGraph
from typing import Any

def cycleCancelling(graph: nx.DiGraph) -> tuple[None | nx.DiGraph, int]:

    workingGraph = graph.copy()

    #memorizing all the nodes with bi > 0 or bi < 0
    availabilities:list[tuple[Any,int]] = []
    requests:list[tuple[Any,int]] = []

    for node, data in workingGraph.nodes(data=True):
        if data["bValue"] > 0:
            availabilities.append((node,data["bValue"]))
        elif data["bValue"] < 0:
            requests.append((node,data["bValue"]))

    #PREPARING GRAPH FOR MAXFLOW ALGORITHM

    #adding s and t nodes to maxFlow graph
    sourceNode = "s"
    suffix = 1
    #checking that there's no node with the same name already in the graph
    while sourceNode in workingGraph:
        sourceNode = f"s_{suffix}"
        suffix += 1
    workingGraph.add_node(sourceNode)
    for node, availability in availabilities:
        workingGraph.add_edge(sourceNode,node,capacity=availability, flow = 0, cost = 0)

    sinkNode = "t"
    suffix = 1
    #checking that there's no node with the same name already in the graph
    while sinkNode in workingGraph:
        sinkNode = f"t_{suffix}"
        suffix += 1
    workingGraph.add_node(sinkNode)
    for node, request in requests:
        workingGraph.add_edge(node,sinkNode,capacity=-request, flow = 0, cost = 0)

    maxFlowValue, workingGraph = maxFlow(workingGraph,sourceNode,sinkNode)

    expectedFlow = 0
    #checking flow correctness
    for node, value in availabilities:
        expectedFlow += value

    """
    To have a valid start solution all out edges from
    source must be saturated. Therefore the max flow value shall be equal to 
    the sum of all maximum capacities
    of the outgoing edges from the node s, which is equal to the sum of all bi positive values in the original graph
    """
    if maxFlowValue < expectedFlow:
        return None, 0

    #cleaning graph after max flow
    workingGraph.remove_node(sourceNode)
    workingGraph.remove_node(sinkNode)

    #CYCLE CANCELLING 

    while True:
        residual = buildResidualGraph(workingGraph)

        #detect negative cycle
        negativeLoop: list[Any] = bellmanFordNegativeCycleDetection(residual)

        #optimal solution reached
        if len(negativeLoop) == 0:
            totCost = 0
            for u,v in workingGraph.edges:
                totCost += workingGraph[u][v]["cost"] * workingGraph[u][v]["flow"]
            return workingGraph, totCost
        
        negativeLoop.append(negativeLoop[0])
        loopEdges: list[tuple[Any,Any, bool]] = [(negativeLoop[i],negativeLoop[i+1], residual[negativeLoop[i]][negativeLoop[i+1]].get("isReverseEdge",False)) for i in range(len(negativeLoop)-1)]

        #find flow augment value in negative cycle
        #setting initial flow value to the residual capacity of the first edge of the cycle
        flowValue : int = residual[loopEdges[0][0]] [loopEdges[0][1]] ["capacity"] - residual[loopEdges[0][0]] [loopEdges[0][1]] ["flow"]

        for u,v, isReverseEdge in loopEdges:
            #if reverse edge take the flow reduction value as flow value to push
            if isReverseEdge:
                flowValue = min(flowValue, -residual[u][v]["flow"])
            else:
                flowValue = min(flowValue, residual[u][v]["capacity"])
                    
        # augment flow in graph
        workingGraph = augmentPath(workingGraph,loopEdges,flowValue)
    