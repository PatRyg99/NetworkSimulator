import random
import itertools

import numpy as np

def generate(density, max_packages, dim=20):
    """
    Function generating intesity matrix with given parametres
    :param list package_size - list with two value, 
                                lower and upper bound for package size, both inclusive
    :param float desity - how dense should the matrix be, number from [0,1-dim]
    :param int dim - dimension of the array

    Places a[i,i] should stay as 0, due to sending packages to themself being pointless
    """
    num_of_packages = int(density * dim**2)
    matrix = np.zeros((dim,dim))
    
    vertices = list(range(dim))

    for _ in range(num_of_packages):
        source = random.choice(vertices)
        target = random.choice(list(
            filter(
                lambda x: x != source and matrix[source,x] == 0,
                vertices
            )
        ))

        matrix[source, target] = random.randint(1, max_packages)

    return matrix

