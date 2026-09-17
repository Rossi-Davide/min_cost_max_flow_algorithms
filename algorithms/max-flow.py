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

#def maxFlow(graph: nx.DiGraph, s: int, t: int):
