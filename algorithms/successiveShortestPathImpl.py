import networkx as nx
from algorithms.dijkstraImpl import dijkstra
from algorithms.augmentPathImpl import augmentPath
from algorithms.residualGraph import buildResidualGraph

from typing import Any

def successiveShortestPath(graph:nx.DiGraph) -> tuple[nx.DiGraph,int]:
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

    for u,v in graph.edges:
        workingGraph[u][v]['flow'] = 0 

    while len(E) > 0:
        k = E.pop()
        l = None
        #building residual graph
        residualGraph = buildResidualGraph(workingGraph)
        #running dijkstra with reduced costs on residual graph
        residualGraph = dijkstra(k, residualGraph)
        for dest_node in D:
            if residualGraph.nodes[dest_node]["dist"] < float('inf'):
                l = dest_node
                break
        if l is None:
            raise ValueError("""The given graph is not a valid graph for max-flow 
            min-cost algorithms because there 
            is a source node with unmet demand""")
        D.remove(l)
        #update potential values in the main graph
        for node in residualGraph.nodes:
            if residualGraph.nodes[node]["dist"] < float('inf'):
                workingGraph.nodes[node]["potential"] -= residualGraph.nodes[node]["dist"]
        
        #find flow increase value in path from k to l
        #set initial value
        flowValue = min(-residualGraph.nodes[l]["e"], residualGraph.nodes[k]["e"])
        pathNodes = []
        currNode = l
        #traverse the path from l to k 
        while currNode != k:
            #append node at the top of the list
            pred = residualGraph.nodes[currNode]["predecessor"]
            #compute residual capacity and update flow value
            residualCap = residualGraph[pred][currNode]["capacity"] - residualGraph[pred][currNode]["flow"]
            flowValue = min(flowValue, residualCap)
            pathNodes.append(currNode)
            currNode = pred
        pathNodes.append(k)
        pathNodes.reverse()
        pathEdges: list[tuple[Any,Any, bool]] = [(pathNodes[i],pathNodes[i+1], residualGraph[pathNodes[i]][pathNodes[i+1]].get("isReverseEdge",False)) for i in range(len(pathNodes)-1)]
        #augment Path in the main graph using the flow value found
        workingGraph = augmentPath(workingGraph,pathEdges,flowValue)
        #update excess value and structures
        workingGraph.nodes[k]["e"] -= flowValue
        if workingGraph.nodes[k]["e"] > 0:
            E.add(k)
        workingGraph.nodes[l]["e"] += flowValue
        if workingGraph.nodes[l]["e"] < 0:
            D.add(l)

    totCost = 0
    for u,v in workingGraph.edges:
        totCost += workingGraph[u][v]["cost"] * workingGraph[u][v]["flow"]
    return workingGraph, totCost
        

    