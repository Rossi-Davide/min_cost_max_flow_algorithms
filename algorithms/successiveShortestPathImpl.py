import networkx as nx
from algorithms.dijkstraImpl import dijkstra
from algorithms.augmentPathImpl import augmentPath
from algorithms.residualGraph import buildResidualGraph

def successiveShortestPath(graph:nx.DiGraph):
    workingGraph = graph.copy()
    E:set = set()
    D:set = set()

    for node in workingGraph.nodes:
        workingGraph.nodes[node]["x"] = 0
        workingGraph.nodes[node]["potential"] = 0
        workingGraph.nodes[node]["e"] = workingGraph.nodes[node]["bValue"]
        if workingGraph.nodes[node]["e"] > 0:
            E.add(node)
        elif workingGraph.nodes[node]["e"] < 0:
            D.add(node)

    while len(E) > 0:
        k = E.pop()
        l = D.pop()
        #building residual graph with no saturated edges from main graph
        residualGraph = buildResidualGraph(workingGraph)
        #running dijkstra with reduced costs on residual graph
        residualGraph = dijkstra(k, residualGraph)
        #TODO: correct implementation of edge case causing termination of the algorithm
        if graph.nodes[l]["predecessor"] is None:
            continue
        #update potential values in the main graph
        for node in residualGraph.nodes:
            workingGraph.nodes[node]["potential"] -= residualGraph.nodes[node]["dist"]
        
        #find flow increase value in path from k to l
        #set initial value
        flowValue = min(-residualGraph.nodes[l]["e"], residualGraph.nodes[k]["e"])
        pathNodes = []
        currNode = l
        #traverse the path from l to k 
        while currNode != k:
            #append node at the top of the list
            pathNodes.insert(0,currNode)
            pred = residualGraph.nodes[currNode]["predecessor"]
            #compute residual capacity and update flow value
            residualCap = residualGraph[pred][currNode]["capacity"] - residualGraph[pred][currNode]["flow"]
            flowValue = min(flowValue, residualCap)
            currNode = pred
        pathNodes.insert(0,k)
        #augment Path in the main graph using the flow value found
        workingGraph = augmentPath(workingGraph,pathNodes,flowValue)
        #update excess value and structures
        workingGraph.nodes[k]["e"] -= flowValue
        if workingGraph.nodes[k]["e"] > 0:
            E.add(k)
        workingGraph.nodes[l]["e"] += flowValue
        if workingGraph.nodes[l]["e"] < 0:
            D.add(l)

        

    