import networkx as nx
from heapq import heapify, heappush, heappop
from typing import Any

"""
Returns a modified version of the graph after running the dijkstra algorithm
storing the distance and predecessor in each node of the graph
"""
def dijkstra(source, graph:nx.DiGraph) -> nx.DiGraph:
    #preparing graph and structures
    for node in graph.nodes:
        node["dist"] = float('inf')
        node["predecessor"] = None
    graph.nodes[source]["dist"] = 0
    heap = []
    heapify(heap)
    heappush(heap,(graph.nodes[source]["dist"],source))
    visited:set = set()

    #unpacking heap
    while len(heap) > 0:
        curr_distance, curr_node = heappop(heap)
        #check if node has already been relaxed
        if curr_node in visited:
            continue
        visited.add(curr_node)
        #relax adjacent nodes
        for u,v in graph.out_edges(curr_node):
            reduced_cost = graph[u][v]["cost"] - graph.nodes[u]["potential"] + graph.nodes[v]["potential"]
            #check if node has a predecessor and whether the cost reduces along new route
            if graph.nodes[v]["predecessor"] is None or graph.nodes[u]["dist"] + reduced_cost < graph.nodes[v]["dist"]:
                #update cost and predecessor of the node
                new_distance = graph.nodes[u]["dist"] + reduced_cost
                graph.nodes[v]["dist"] = new_distance
                graph.nodes[v]["predecessor"] = u
                #push node with updated distance in the heap
                heappush(heap,(new_distance, v))
            
    return graph

