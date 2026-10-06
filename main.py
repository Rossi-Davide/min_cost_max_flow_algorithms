import networkx as nx
from algorithms.maxFlowImpl import maxFlow
from loadFromFile import load_directed_graph

if __name__ != "__main__":
    exit()

graph = load_directed_graph("graph_1_simple.txt", separator=" ")
if graph is None:
    raise RuntimeError("Unsuccessful parsing of file")
#parse string values to int
for node in graph.nodes:
    if graph.nodes[node].get("bValue",False) and graph.nodes[node]["bValue"].isdigit():
        graph.nodes[node]["bValue"] = int(graph.nodes[node]["bValue"])
for u, v, data in graph.edges(data=True):
    if data.get("capacity", False):
        data["capacity"] = int(data["capacity"])
    if data.get("cost", False):
        data["cost"] = int(data["cost"])
