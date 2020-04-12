import numpy as np

import scripts.route as route

class Package():
    def __init__(self, size, source, target):
        self.size = size
        self.source = source
        self.target = target
        
        self.time = 0
        self.current = source
        self.success = self.current == self.target

    def send(self, G):
        return route.shortest_generator(G, self)

def packages_from_matrix(intensity_matrix):
    """
    Generates list of packages from a given intensity_matrix
    """
    packages = []

    for (x,y), value in np.ndenumerate(intensity_matrix):
        if value != 0:
            packages.append(Package(int(value), x, y))

    return packages