import networkx as nx
import argparse
from loadFromFile import load_directed_graph
from algorithms.cycleCancelling import cycleCancelling
from algorithms.successiveShortestPathImpl import successiveShortestPath

if __name__ != "__main__":
    exit()


parser = argparse.ArgumentParser()
parser.add_argument('--graph', required=True)
args = parser.parse_args()

graph = load_directed_graph(args.graph, separator=" ")
if graph is None:
    raise RuntimeError("Unsuccessful parsing of file")
#parse string values to int
for node in graph.nodes:
    if graph.nodes[node].get("bValue",False):
        graph.nodes[node]["bValue"] = int(graph.nodes[node]["bValue"])
for u, v, data in graph.edges(data=True):
    if data.get("capacity", False):
        data["capacity"] = int(data["capacity"])
    if data.get("cost", False):
        data["cost"] = int(data["cost"])

def print_graph_summary(label, graph):
    print(f"\n{label}")
    print(f"  Nodes: {graph.number_of_nodes()}")
    print(f"  Edges: {graph.number_of_edges()}")
    print("  Node details:")
    for node, attrs in graph.nodes(data=True):
        print(f"    - {node}: {attrs}")
    print("  Edge details:")
    for u, v, attrs in graph.edges(data=True):
        print(f"    - {u} -> {v}: {attrs}")

print(f"Loaded graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges")
print_graph_summary("Original graph", graph)

print(f'Running cycle cancelling algorithm')
cycle_cancelling_graph, cost = cycleCancelling(graph)
if cycle_cancelling_graph is None:
    print("Error while running cycle cancelling algorithm")
else:
    print(f'Cost from cycle cancelling solution: {cost}')
    print_graph_summary("Cycle cancelling graph", cycle_cancelling_graph)

print(f'Running successive shortest path algorithm')
ssp_graph, cost = successiveShortestPath(graph)
if ssp_graph is None:
    print("Error while running successive shortest path algorithm")
else:
    print(f'Cost from successive shortest path solution: {cost}')
    print_graph_summary("Successive shortest path graph", ssp_graph)