import networkx as nx

def shortest_generator(G, package):
    """
    Generator of path for the given package in graph G.
    1) The shortest path is found for package
    2) Generators yields current node and performs one action: v0,e1,v1,...,en,vn
    3) If package cannot take a shortest path due to capacity of an edge
        being to low, the edge is removed from the graph - G2, and shortest
        path in G2 is being found
    4) If no such path available or 5 attempts have been made to find such path
        the package is waiting one round in the current vertice
    5) When package arrives at the target, its success flag is set to true
    """
    path = nx.shortest_path(G, source=package.source, target=package.target)

    edges_to_remove = []
    yield_source = True
    edge_taken = False
    attempts = 0
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
        if current_edge["capacity"] > current_edge["flow"] + package.size:
            G.nodes[package.current]['color'] = "g"

            current_edge['packages'] += 1
            current_edge['flow'] += package.size
            current_edge['color'] = "r"

            edge_taken = True
            package.current = path[step]
            step += 1

        # Otherwise remove edge from graph and find new shortest path
        else:
            G_copy = G.copy()
            edges_to_remove.append(edge)
            
            G_copy.remove_edges_from(edges_to_remove)
            attempts += 1

            try:
                # If more than 5 attempts than call no path found
                if attempts >= 5:
                    raise nx.NetworkXNoPath 

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
                package.waited = True
                pass
        
        attempts = 0
        edges_to_remove = []
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


def shortest_weight_path(G, package):
    """
    Algorithm that finds shortest weighted path for package.
    Than all edges on the path are weighted by the given package's size.
    """
    unavailable = True
    attempts = 10
    G_copy = G.copy()

    # Choosing shortest path with weight
    while unavailable and attempts > 0:
        unavailable = False

        try:
            path = nx.shortest_path(
                G_copy, source=package.source, 
                target=package.target,
                weight = 'weight'
            )
        except nx.NetworkXNoPath:
            return False

        for i in range(1, len(path)):
            if G[path[i-1]][path[i]]["capacity"] <= G[path[i-1]][path[i]]["flow"] + package.size:
                unavailable = True
                G_copy.remove_edge(path[i-1], path[i])
                attempts -= 1
                break


    # No shortest path found
    if attempts <= 0:
        return False

    # Adding weight onto the path
    for i in range(1, len(path)):
        current_edge = G[path[i-1]][path[i]]
        current_edge["flow"] += package.size
        current_edge["weight"] = current_edge["flow"] / current_edge["capacity"]
        current_edge["color"] = "r"
        current_edge["packages"] += 1
    
    return True
