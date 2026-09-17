import networkx as nx

def augmentPathBFS(graph: nx.DiGraph, s:int) -> list[tuple[int, int]]:
    nodeLabels = [(-1, -1) for _ in range(graph.number_of_nodes())]
    nodeLabels[s] = (s, -1)
    visited:set[int] = set()
    queue = [s]

    while len(queue) > 0:
        index:int = queue.pop(0)
        visited.add(index)
        for u, v, data in graph.out_edges(index, data=True):
            if v in visited:
                continue
            pred, predj_flow = nodeLabels[index]
            new_flow = 0
            if predj_flow < 0:
                new_flow = data["capacity"] - data["flow"]
            else:
                new_flow = min(predj_flow, data["capacity"] - data["flow"])
            nodeLabels[v] = (index, new_flow)
            queue.append(v)
            
    return nodeLabels

def maxFlow(graph: nx.DiGraph, s: int, t: int):
    residualGraph = graph.copy()

    for u, v in residualGraph.edges:
        if "flow" not in residualGraph[u][v]:
            residualGraph[u][v]["flow"] = 0

    optimalState = False

    while not optimalState:
        nodeLabels = augmentPathBFS(residualGraph,s)

        #first predecessor and bottleneck value for augmenting flow
        firstPred, augmFlow = nodeLabels[t]
        currNode = t
        #no new augmenting path found, algorithm stops for optimality condition
        if firstPred == -1:
            optimalState = True
            continue
        
        while currNode != s:
            pred, flow = nodeLabels[currNode]
            residualGraph.edges[pred,currNode]["flow"] = residualGraph.edges[pred,currNode]["flow"] + augmFlow
            if not residualGraph.has_edge(currNode, pred):
                residualGraph.add_edge(currNode, pred, capacity=0, flow=0, isResidualEdge = True)

            residualGraph.edges[currNode, pred]["flow"] = residualGraph.edges[currNode, pred]["flow"] - augmFlow

            currNode = pred
    