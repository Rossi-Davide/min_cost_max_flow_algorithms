import networkx as nx
from algorithms.maxFlowImpl import maxFlow 
from typing import Any

"""
Builds a residual graph by adding reverse edges 
and eliminating edges with saturated flow
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

    #removing saturated edges
    toDelete: list[tuple[Any,Any]] = []

    for u,v in R.edges:
        if R[u][v]["flow"] == R[u][v]["capacity"]:
            toDelete.append((u,v))

    for u,v in toDelete:
        R.remove_edge(u,v)

    return R

def cycleCancelling(graph: nx.DiGraph):

    maxFlowGraph = graph.copy()

    #memorizing all the nodes with bi > 0 or bi < 0
    availabilities:list[tuple[Any,int]] = []
    requests:list[tuple[Any,int]] = []

    for node, data in maxFlowGraph.nodes:
        if data["bValue"] > 0:
            availabilities.append((node,data["bValue"]))
        elif data["bValue"] < 0:
            requests.append((node,data["bValue"]))

    #adding s and t to maxFlow graph
    maxFlowGraph.add_node("s")
    for node, availability in availabilities:
        maxFlowGraph.add_edge("s",node,capacity=availability, flow = 0, cost = 0)

    maxFlowGraph.add_node("t")
    for node, request in availabilities:
        maxFlowGraph.add_edge("t",node,capacity=-request, flow = 0, cost = 0)

    maxFlowValue, workingGraph = maxFlow(maxFlowGraph,"s","t")

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
        return "No acceptable solution found"

    
    
    

    