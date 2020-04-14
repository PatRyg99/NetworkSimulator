import os

import pandas as pd

import scripts.graph as graph
import scripts.intensity_matrix as intensity_matrix
from scripts.simulator import Simulator
from scripts.package import Package, packages_from_matrix

class Pipeline():
    def __init__(self, topology, capacity_param, package_size, 
                    density, no_edge_failure, repeat, directory):
        self.topology = topology
        self.capacity_param = capacity_param
        self.package_size = package_size
        self.density = density
        self.no_edge_failure = no_edge_failure
        self.repeat = repeat
        self.directory = directory

    def run(self):
        """
        Method running stats for given params and saving into file
        """
        G = graph.generate(
            "topologies/"+self.topology+".txt", 
            capacity_param = self.capacity_param
        )
        
        matrix = intensity_matrix.generate(self.package_size, self.density)
        packages = packages_from_matrix(matrix)

        simulator = Simulator(G, packages)

        df = simulator.run_in_place_stats(
            p=self.no_edge_failure,
            repeat=self.repeat
        )

        # Saving data
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        df.to_csv(self.directory+"/data.txt", index=False)
        self.get_config().to_csv(self.directory+"/config.txt", index=False)


    def preview(self):
        G = graph.generate(
            "topologies/"+self.topology+".txt", 
            capacity_param = self.capacity_param
        )

        matrix = intensity_matrix.generate(self.package_size, self.density)
        packages = packages_from_matrix(matrix)

        simulator = Simulator(G, packages)

        stats = simulator.run_in_place(
            p=self.no_edge_failure,
        )

        df = pd.DataFrame([stats], columns=["infallibility", "edge_broke", "failure"])
        print(df.to_string(index=False))
        print("----------------------------------------------------------------------")
        print(self.get_config().to_string(index=False))


    def get_config(self):
        columns = ["topology", "capacity_param", "package_size", "density", "no_edge_failure"]
        config = [(
            self.topology, self.capacity_param, self.package_size, 
            self.density, self.no_edge_failure
        )]

        return pd.DataFrame(config, columns=columns)