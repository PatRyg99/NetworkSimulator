import time
import copy
import random
from statistics import mean
from random import shuffle
from IPython.display import clear_output

import pandas as pd

import scripts.graph as graph
import scripts.route as route

class Simulator():
    """
    Simulator class that runs simulation of given packages for given graph
    """
    def __init__(self, G, packages):
        self.G = G
        self.packages = packages
        self.entire_capacity = len(self.packages)
        self.mean_size = mean(p.size for p in self.packages)

    def delay(self):
        """
        Calculates delay of package of the graph, based on capacity and flows of the edges
        """
        edge_sum = sum(
            self.G[n1][n2]['packages']/
            (self.G[n1][n2]['capacity']/self.mean_size - self.G[n1][n2]['packages'])
            for (n1,n2) in self.G.edges()
        )

        return (1/self.entire_capacity)*edge_sum


    def run_in_place_stats(self, p, repeat):
        """
        Runs run in place method "repeat" number of times.
        Returns pandas dataframe with:
            delay,
            if edge broke,
            if failure
        """
        stats = []
        for _ in range(repeat):
            stats.append(self.run_in_place(p=p, draw=False))
            
        df = pd.DataFrame(stats, columns=["delay", "edge_broke", "failure"])
        return df


    def run_in_place(self, p = 90, draw = True):
        """
        In place simulation with deterministic paths for each pair of vertices.
        Method returns True when for all packages the path was able to be found.
        Graph with flows is being drawn and delay counted.

        Given parameter path tells what is a chance of graph not being damaged,
        meaning probability of a failure of an edge.
        """
        broken_package = None
        broken_edge = False

        # Checking if edge to be broken
        if random.randint(0,100) > p:
            index = random.randint(0,len(self.G.edges())-1)
            edge = [e for i,e in enumerate(self.G.edges) if i == index]

            self.G[min(*edge)][max(*edge)]['failed'] = True
            self.G[min(*edge)][max(*edge)]['flow'] = self.G[min(*edge)][max(*edge)]['capacity']
            self.G[min(*edge)][max(*edge)]['color'] = "k"

            broken_edge = True

        # Finding paths for all packages
        shuffle(self.packages)
        for package in self.packages:
            if not route.shortest_weight_path(self.G, package):
                broken_package = package
                break
            
        if draw:
            graph.draw(self.G)

        delay = self.delay()
        graph.clear_simulation(self.G)

        # If no path for package invoke failure
        if broken_package:
            if draw:
                print("Failure for package")
                print("Source: ", broken_package.source)
                print("Target: ", broken_package.target)
                print("Size: ", broken_package.size)

            return delay, broken_edge, True

        return delay, broken_edge, False



    def run(self, timeout, timelapse = 1, reload_flag = False, draw = True):
        """
        Runs simulation for simulator object.
        :param int timeout - how many rounds should the simulation take
        :param int timelapse - time of a round in seconds

        For each package the generator is being invoked once in each round.
        In each round the graph is being drawn with shown vertices and edges were
        currently packages are.
        """
        rounds = 0
        timer = 0
        delay = []

        input_packages = copy.deepcopy(self.packages)
        package_routes = [(p,p.send(self.G)) for p in self.packages]

        while (False in [p.success for p in self.packages]) and timer < timeout: 

            # Shuffling packages order, to simulate threading
            shuffle(package_routes)
            for p, route in package_routes:
                if not p.success:
                    next(route)
    
            # Print updated graph
            if draw:
                clear_output(wait=True)
                graph.draw(self.G)
            rounds += 1

            # Incrementing timer and counting delay only on edge move
            if rounds % 2 == 0 and (False in [p.success for p in self.packages]):
                timer += 1
                delay.append((timer, self.delay()))

                reload_packages = copy.deepcopy(input_packages)
                self.packages.extend(reload_packages)
                package_routes.extend([(p,p.send(self.G)) for p in reload_packages])

            if draw:
                print("Timer: ", timer)

            time.sleep(timelapse)
                
        # Printing statistics
        print("\n"+pd.DataFrame(delay, columns=["Timer","Delay"]).to_string(index=False))

        #data = [[p.source, p.target, p.time, p.success, p.waited] for p in self.packages]
        #df = pd.DataFrame(data, columns=["Source", "Target", "Time", "Success", "Waited"])
        #print("\n"+df.to_string(index=False))
        print("Total packages: ", len(self.packages))
        print("Waited: ", sum(1 for p in self.packages if p.waited == True))