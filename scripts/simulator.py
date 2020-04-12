import time
from IPython.display import clear_output
from IPython.display import HTML

import pandas as pd

import scripts.graph as graph

class Simulator():
    """
    Simulator class that runs simulation of given packages for given graph
    """
    def __init__(self, G, packages):
        self.G = G
        self.packages = packages

    def run(self, timeout, timelapse = 1):
        package_routes = [(p,p.send(self.G)) for p in self.packages]

        timer = 0
        while (False in [p.success for p in self.packages]) and timer // 2 < timeout: 
            for p, route in package_routes:
                if not p.success:
                    next(route)
    
              
            clear_output(wait=True)
            graph.draw(self.G)

            # Incrementing timer only if not ended
            if (False in [p.success for p in self.packages]):
                timer += 1

            print("Timer: ", timer // 2)

            time.sleep(timelapse)


        # Printing statistics
        data = [[p.source, p.target, p.time, p.success] for p in self.packages]
        df = pd.DataFrame(data, columns=["Source", "Target", "Time", "Success"])
        print("\n"+df.to_string(index=False))