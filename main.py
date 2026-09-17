import networkx as nx

if __name__ != "__main__":
    exit

s = 0
t = 4

capacities = [
    [0, 3, 1, 0, 3],
    [0, 0, 2, 0, 0],
    [0, 0, 0, 1, 6],
    [0, 0, 0, 0, 2],
    [0, 0, 0, 0, 0],
]

costs = [
    [0, 1, 0, 0, 2],
    [0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0],
]

G = nx.DiGraph()
for i in range(len(capacities)):
    for j in range(len(capacities[i])):
        if capacities[i][j] > 0:
            G.add_edge(i, j, capacity=capacities[i][j], cost=costs[i][j])

print("Nodes:", list(G.nodes()))
print("Edges:", list(G.edges(data=True)))