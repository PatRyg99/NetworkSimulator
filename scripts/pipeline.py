import os

import pandas as pd
import numpy as np

import scripts.graph as graph
import scripts.intensity_matrix as intensity_matrix
from scripts.simulator import Simulator
from scripts.package import Package, packages_from_matrix

class Pipeline():
    """
    High level launcher, taking configuration and running all components to create and test the graph.
    Utilizing strategy pattern to provide easy config switch.
    """
    def __init__(self, topology, capacity_param, avg_package_size,
                    max_packages, density, no_edge_failure, repeat, directory):
        self.topology = topology
        self.capacity_param = capacity_param
        self.avg_package_size = avg_package_size
        self.max_packages = max_packages
        self.density = density
        self.no_edge_failure = no_edge_failure
        self.repeat = repeat
        self.directory = directory

    def run(self, T_interval, T_step, int_matrix = None):
        """
        Method running stats for given params and saving into file
        """
        G = graph.generate(
            "topologies/"+self.topology+".txt", 
            capacity_param = self.capacity_param
        )
        
        if type(int_matrix) is not np.ndarray:
            matrix = intensity_matrix.generate(self.density, self.max_packages)
        else:
            matrix = int_matrix

        packages = packages_from_matrix(matrix, self.avg_package_size)

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

        # Printing infallibility in percentages
        infallibilities = []
        for T_max in np.arange(T_interval[0], T_interval[1], T_step):

            seriesObj = df.apply(
                lambda x: True if x['delay'] < T_max and x['failure'] == False  else False , axis=1
            )

            infallibilities.append((T_max, 100*len(seriesObj[seriesObj == True].index)//self.repeat))

        
        print("Infallibility Pr[delay < T_max]:")
        
        failures = df.apply(lambda x:  True if x['failure'] == True else False, axis=1)
        print("Failures: {}\n".format(len(seriesObj[failures == True].index)))

        df = pd.DataFrame(infallibilities, columns=["T_max","Infallibility [%]"])
        print(df.to_string(index=False))

        return matrix


    def preview(self, int_matrix = None):
        """
        Method running preview of configuration on one example, showing the graph itself.
        """
        G = graph.generate(
            "topologies/"+self.topology+".txt", 
            capacity_param = self.capacity_param
        )

        if type(int_matrix) is not np.ndarray:
            matrix = intensity_matrix.generate(self.density, self.max_packages)
        else:
            matrix = int_matrix

        packages = packages_from_matrix(matrix, self.avg_package_size)

        simulator = Simulator(G, packages)

        stats = simulator.run_in_place(
            p=self.no_edge_failure,
        )

        df = pd.DataFrame([stats], columns=["delay", "edge_broke", "failure"])
        
        print("----------------------------------------------------------------------")
        print(df.to_string(index=False))
        print("----------------------------------------------------------------------")
        print(self.get_config().to_string(index=False))


    def get_config(self):
        columns = ["topology", "capacity_param", "avg_package_size", "density", "no_edge_failure"]
        config = [(
            self.topology, self.capacity_param, self.avg_package_size, 
            self.density, self.no_edge_failure
        )]

        return pd.DataFrame(config, columns=columns)