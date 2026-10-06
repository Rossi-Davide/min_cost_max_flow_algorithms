import networkx as nx
from algorithms.dijkstraImpl import dijkstra
from algorithms.augmentPathImpl import augmentPath

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
        workingGraph = dijkstra(k, workingGraph)
        #TODO: correct implementation of edge case causing termination of the algorithm
        if graph.nodes[l]["predecessor"] is None:
            continue
        for node in workingGraph.nodes:
            workingGraph.nodes[node]["potential"] -= workingGraph.nodes[node]["dist"]
        #find flow increase value in path from k to l

        #set initial value
        flowValue = min(-workingGraph.nodes[l]["e"], workingGraph.nodes[k]["e"])
        pathNodes = []
        currNode = l
        #traverse the path from l to k 
        while currNode != k:
            #append node at the top of the list
            pathNodes.insert(0,currNode)
            pred = workingGraph.nodes[currNode]["predecessor"]
            #compute residual capacity and update flow value
            residualCap = workingGraph[pred][currNode]["capacity"] - workingGraph[pred][currNode]["flow"]
            flowValue = min(flowValue, residualCap)
            currNode = pred
        pathNodes.insert(0,k)
        #augment Path using the flow value found
        workingGraph = augmentPath(workingGraph,pathNodes,flowValue)


        

    