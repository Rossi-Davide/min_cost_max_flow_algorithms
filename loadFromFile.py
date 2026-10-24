import networkx as nx
from pathlib import Path

GRAPH_DIR = Path(__file__).parent / "graphs"

def load_directed_graph(filepath: str, separator:str) -> nx.DiGraph | None:
    """
    Reads a directed graph from given filepath using given separator. 
    Returns a directed nx graph if operation is successful or None if it there are problems. 
    By default, all labels and values are considered strings

    File is expected to be in the following format:

    First two lines of the file are in the following format:
    nodes "list of node properties names"
    edges "list of edge properties names"

    and give an indication of which properties nodes and edges have.
    Following, is a series of lines that either describe a node or an edge. 

    Using the following format for node lines:
    n node_label node_properties_values[]

    and the following for edge lines:
    e first_node second_node edge_properties_values[]
    """
    G = nx.DiGraph()

    path = GRAPH_DIR / filepath

    with open(path,"r") as f:
        #read formatting of node lines and attributes
        node_format = f.readline()
        node_format = node_format.strip()
        node_format_parts = node_format.split(separator)
        edge_format = f.readline()
        edge_format = edge_format.strip()
        edge_format_parts = edge_format.split(separator)
        #file in wrong format
        if edge_format_parts[0] != "edges" or node_format_parts[0] != "nodes":
            return None
        nodes_properties = [node_format_parts[i] for i in range(1,len(node_format_parts))]
        edge_properties = [edge_format_parts[i] for i in range(1,len(edge_format_parts))]
        # read until EOF
        for line in f:
            #read line of the node
            line = line.strip()
            parts = line.split(separator)
            #check that the line is for a node and that it's in the correct format
            if parts[0] == 'n' and len(parts) == len(nodes_properties) + 2:
                #label for the node
                node_label = parts[1]
                G.add_node(node_label)
                #set node properties
                for i in range(len(nodes_properties)):
                    property_name = nodes_properties[i]
                    value = parts[i + 2]
                    G.nodes[node_label][property_name] = value
            elif parts[0] == 'e' and len(parts) == len(edge_properties) + 3:
                #read nodes of edge
                u = parts[1]
                v = parts[2]
                G.add_edge(u,v)
                #set properties for edge
                for i in range(len(edge_properties)):
                    property_name = edge_properties[i]
                    value = parts[i + 3]
                    G[u][v][property_name] = value 
            else:
                #skip line in wrong format
                continue
    return G
        
