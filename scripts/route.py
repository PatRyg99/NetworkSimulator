import networkx as nx

def shortest_generator(G, package):
    path = nx.shortest_path(G, source=package.source, target=package.target)

    yield_source = True
    edge_taken = False
    step = 1
    
    while package.current != package.target:
        edge_taken = False

        # Yield current vertice and show it
        if yield_source:
            G.nodes[package.current]['color'] = "r"
            yield package.current
        else:
            yield_source = True

        # Find next edge from the path and show it 
        edge = (package.current, path[step])
        current_edge = G[min(edge)][max(edge)]

        # Go through edge if capacity is enough
        if current_edge["capacity"] >= current_edge["flow"] + package.size:
            G.nodes[package.current]['color'] = "g"

            current_edge['flow'] += package.size
            current_edge['color'] = "r"

            edge_taken = True
            package.current = path[step]
            step += 1

        # Otherwise remove edge from graph and find new shortest path
        else:
            G_copy = G.copy()
            G_copy.remove_edge(*edge)

            try:
                # Check for new path
                new_path = nx.shortest_path(G_copy, source=package.current, target=package.target)
                
                # If new path exists than take it
                G.nodes[package.current]['color'] = "g"
                path = new_path
                step = 1
                yield_source = False
                continue

            except nx.NetworkXNoPath:
                # If no new path than wait in current node
                pass

        package.time += 1
        yield package.current

        # Reset edges color and flow if not waiting
        if edge_taken:
            current_edge['flow'] -= package.size
        
            if current_edge['flow'] == 0:
                current_edge['color'] = "b"


    # Showing reached target
    G.nodes[package.current]['color'] = "r"
    yield package.current

    # Ending simulation
    G.nodes[package.current]['color'] = "g"
    package.success = True
    yield package.current