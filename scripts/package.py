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