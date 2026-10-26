import networkx as nx
from algorithms.dijkstraImpl import dijkstra
from .maxFlowImpl import maxFlow
from .residualGraph import buildResidualGraph

def a_graph(graph:nx.DiGraph) -> nx.DiGraph:
    a_graph = nx.DiGraph()
    a_graph.add_nodes_from(graph)
    for u,v in graph.edges:
        if graph[u][v]["cost"] - graph.nodes[u]["potential"] + graph.nodes[v]["potential"] == 0:
            a_graph.add_edge(u, v, capacity= graph[u][v]["capacity"], flow=graph[u][v]["flow"])
    return a_graph


def primal_dual(graph: nx.DiGraph) -> tuple[nx.DiGraph,int]:
    workingGraph = graph.copy()

    e_s = 0 

    for node in workingGraph.nodes:
        workingGraph.nodes[node]["x"] = 0
        workingGraph.nodes[node]["potential"] = 0
        if workingGraph.nodes[node]["bValue"] > 0:
            e_s += workingGraph.nodes[node]["bValue"]
    e_t = - e_s
    outgoing_flow = 0

    for u,v in graph.edges:
        workingGraph[u][v]["flow"] = 0
 
    #adding s and t nodes to maxFlow graph
    sourceNode = "s"
    suffix = 1
    #checking that there's no node with the same name already in the graph
    while sourceNode in workingGraph:
        sourceNode = f"s_{suffix}"
        suffix += 1
    workingGraph.add_node(sourceNode, e=e_s, potential=0, x=0)
    sources = [node for node in graph.nodes if graph.nodes[node]["bValue"] > 0] 
    for node in sources:
        workingGraph.add_edge(sourceNode,node,capacity=graph.nodes[node]["bValue"], flow = 0, cost = 0)

    sinkNode = "t"
    suffix = 1
    #checking that there's no node with the same name already in the graph
    while sinkNode in workingGraph:
        sinkNode = f"t_{suffix}"
        suffix += 1
    workingGraph.add_node(sinkNode, e=e_t, potential=0, x=0)
    sinks = [node for node in graph.nodes if graph.nodes[node]["bValue"] < 0]
    for node in sinks:
        workingGraph.add_edge(node,sinkNode,capacity=-graph.nodes[node]["bValue"], flow = 0, cost = 0)

    while (e_s - outgoing_flow) > 0:
        R = buildResidualGraph(workingGraph)
        R = dijkstra(sourceNode, R)

        if R.nodes[sinkNode]["dist"] == float('inf'):
            raise ValueError("""The given graph is not a valid graph for max-flow 
            min-cost algorithms because there 
            is a source node with unmet demand""")

        #update potential values in the main graph
        for node in R.nodes:
            if R.nodes[node]["dist"] < float('inf'):
                workingGraph.nodes[node]["potential"] -= R.nodes[node]["dist"]

        as_graph = a_graph(workingGraph)
        flowValue, maxFlowGraph = maxFlow(as_graph, sourceNode, sinkNode)
        for u, v in maxFlowGraph.edges:
            workingGraph[u][v]["flow"] = maxFlowGraph[u][v]["flow"]
        #computing outgoing flow
        outgoing_flow = flowValue

    totCost = 0
    for u,v in workingGraph.edges:
        totCost += workingGraph[u][v]["cost"] * workingGraph[u][v]["flow"]
    return workingGraph, totCost

