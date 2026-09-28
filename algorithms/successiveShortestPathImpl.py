import networkx as nx
from algorithms.dijkstraImpl import dijkstra
from algorithms.augmentPathImpl import augmentPath

def successiveShortestPath(graph:nx.DiGraph):
    workingGraph = graph.copy()
    E:set = set()
    D:set = set()

    for node in workingGraph.nodes:
        node["x"] = 0
        node["potential"] = 0
        node["e"] = node["bValue"]
        if node["e"] > 0:
            E.add(node)
        elif node["e"] < 0:
            D.add(node)

    while len(E) > 0:
        k = E.pop()
        l = D.pop()
        workingGraph = dijkstra(k, workingGraph)
        for node in workingGraph.nodes:
            node["potential"] -= node["dist"]
        #find flow increase value in path from k to l
        flowValue = min(-graph.nodes[l]["e"], graph.nodes[k]["e"])
        pathNodes = []
        currNode = l
        while currNode != k:
            pathNodes.insert(0,currNode)
            pred = graph.nodes[currNode]["predecessor"]
            residual = graph[pred][currNode]["capacity"] - graph[pred][currNode]["flow"]
            flowValue = min(flowValue, residual)
            currNode = pred
        pathNodes.insert(0,k)
        #augmentPath
        workingGraph = augmentPath(workingGraph,pathNodes,flowValue)
        

    