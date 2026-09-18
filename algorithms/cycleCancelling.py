import networkx as nx
from algorithms.maxFlowImpl import maxFlow 
from typing import Any

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

    
    

    