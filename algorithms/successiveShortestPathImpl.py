import networkx as nx

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

    

    