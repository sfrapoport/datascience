from __future__ import division
from linear_algebra import *
import math
import random
import matplotlib.pyplot as plt

class KMeans:
    """cluster using kmeans algorithm"""
    def __init__(self, k):
        self.k = k      # number of clusters
        self.means = None   # means of clusters

    def classify(self, input):
        """return index of cluster closest to input"""
        return min(range(self.k),
        key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):
        # select k random points to start with
        self.means = random.sample(inputs, self.k)
        assignments = None
        while True:
            # Find new assignments
            new_assignments = map(self.classify, inputs)

            # If no assignments changed, DONE
            if assignments == new_assignments:
                primarycolors = [(1,0,0), (0,1,0), (0,0,1)]
                colors = [primarycolors[i] for i in assignments] 
                x = [pair[0] for pair in inputs]
                y = [pair[1] for pair in inputs]
                plt.scatter(x, y, c=colors)
                plt.show()
                return

            # Else keep new assignment
            assignments = new_assignments

            #Compute new means
            for i in range(self.k):
                # Find all points assigned to cluster i
                i_points = [p for p, a in zip(inputs, assignments) if a==i]

                # Make sure i_points is not empty so don't divide by 0
                if i_points:
                    self.means[i] = vector_mean(i_points)

if __name__ == "__main__":

    inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]

    random.seed(0) # so you get the same results as me
    clusterer = KMeans(3)
    clusterer.train(inputs)
    print "3-means:"
    print clusterer.means
    print
    
    random.seed(0)
    clusterer = KMeans(2)
    clusterer.train(inputs)
    print "2-means:"
    print clusterer.means
    print

    import numpy as np
    import matplotlib.pyplot as plt

    
