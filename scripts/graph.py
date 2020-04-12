import numpy as np
import networkx as nx
import pylab

from networkx.drawing.nx_agraph import graphviz_layout

def generate(file_name, capacity_range):
    """
    Generates graph from the given file
    """
    edges_array = np.loadtxt(file_name, delimiter=',')
    G = nx.from_numpy_array(edges_array)
    
    capacity = np.random.random_integers(low=capacity_range[0],
                                        high=capacity_range[1],
                                        size=len(G.edges()))
    
    for i, (n1,n2) in enumerate(G.edges()):
        G[n1][n2]['capacity'] = (G.degree[n1]+G.degree[n2])
        G[n1][n2]['flow'] = 0
        G[n1][n2]['color'] = "b"

    for v in G.nodes():
        G.nodes[v]['color'] = "g"
    
    return G

def draw(G):
    """
    Draws given graph as a figure
    """
    pylab.figure(1, figsize=(8,8))
    
    pos = graphviz_layout(G, prog="neato")
    edge_labels = {
        (n1,n2): str(G[n1][n2]['flow']) + " / " + str(G[n1][n2]['capacity']) 
        for (n1,n2) in G.edges()
    }
    
    edge_colors = [G[n1][n2]['color'] for (n1,n2) in G.edges()]
    node_colors = [v[1]['color'] for v in G.nodes(data=True)]
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(G, pos)
    
    print("Vertices: ", len(G.nodes()))
    print("Edges: ", len(G.edges()))
    print("Capacity: ", sum(G[n1][n2]["capacity"] for (n1,n2) in G.edges()))
    
    pylab.show()