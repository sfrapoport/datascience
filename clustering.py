from __future__ import division
from linear_algebra import *
import math
import random
import matplotlib.pyplot as plt
import numpy
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
                # primarycolors = [(1,0,0), (0,1,0), (0,0,1)]
                # colors = [primarycolors[i] for i in assignments] 
                # x = [pair[0] for pair in inputs]
                # y = [pair[1] for pair in inputs]
                # plt.scatter(x, y, c=colors)
                # plt.show()
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

def squared_clustering_errors(inputs, k):
    """sums the squares of the errors for clustering with k means"""
    kmeans = KMeans(k)
    kmeans.train(inputs)
    means = kmeans.means
    assignments = map(kmeans.classify, inputs)

    return sum(squared_distance(input, means[cluster]) for input, cluster in zip(inputs, assignments))

# if __name__ == "__main__":

inputs = [[-14,-5],[13,13],[20,23],[-19,-11],[-9,-16],[21,27],[-49,15],[26,13],[-46,5],[-34,-1],[11,15],[-49,0],[-22,-16],[19,28],[-12,-8],[-13,-19],[-41,8],[-11,-6],[-25,-9],[-18,-3]]

    # random.seed(0) # so you get the same results as me
    # clusterer = KMeans(3)
    # clusterer.train(inputs)
    # print "3-means:"
    # print clusterer.means
    # print
    
    # random.seed(0)
    # clusterer = KMeans(2)
    # clusterer.train(inputs)
    # print "2-means:"
    # print clusterer.means
    # print

    # ks = range(1, len(inputs) + 1)
    # errors = [squared_clustering_errors(inputs, k) for k in ks]

    # plt.plot(ks, errors)
    # plt.xticks(ks)
    # plt.xlabel("k")
    # plt.ylabel("total squared error")
    # plt.title("Total Error vs. # of Clusters")
    # plt.show()
    
#path_to_png_file = "./image.png"
#import matplotlib.image as mpimg
#img = mpimg.imread(path_to_png_file)
#pixels = [pixel for row in img for pixel in row]
#clusterer = KMeans(5)
#clusterer.train(pixels)
#
#def recolor(pixel):
#    cluster = clusterer.classify(pixel)
#    return clusterer.means[cluster]
#
#new_image = [[recolor(pixel) for pixel in row] for row in img]
#
#plt.imshow(new_image)
#plt.axis('off')
#plt.show()

# Bottom up clustering

def is_leaf(cluster):
    return len(cluster) == 1

def get_children(cluster):
    if is_leaf(cluster):
        raise TypeError("a leaf cluster has no children")
    else:
        return cluster[1]

def get_values(cluster):
    if is_leaf(cluster):
        return cluster  # is already a 1-tupble containing value
    else:
        return [value
                for child in get_children(cluster)
                for value in get_values(child)]

def cluster_distance(cluster1, cluster2, distance_agg=min):
    return distance_agg([distance(input1, input2)
        for input1 in get_values(cluster1)
        for input2 in get_values(cluster2)])

def get_merge_order(cluster):
    if is_leaf(cluster):
        return float('inf')
    else:
        return cluster[0]

def bottom_up_cluster(inputs, distance_agg=min):
    # Start with every leaf
    clusters = [(input,) for input in inputs]
    while len(clusters) > 1:
        c1, c2 = min([(cluster1, cluster2)
            for i, cluster1 in enumerate(clusters)
            for cluster2 in clusters[:i]],
            key = lambda (x,y): cluster_distance(x, y, distance_agg))
        clusters = [c for c in clusters if c != c1 and c != c2]
        merged_cluster = (len(clusters), [c1, c2])
        clusters.append(merged_cluster)
    return clusters[0]

def generate_clusters(base_cluster, num_clusters):
    clusters = [base_cluster]
    while len(clusters) < num_clusters:
        next_cluster = min(clusters, key=get_merge_order)
        clusters = [c for c in clusters if c != next_cluster]
        clusters.extend(get_children(next_cluster))
    return clusters

base_cluster = bottom_up_cluster(inputs, numpy.mean)
print base_cluster

three_clusters = [get_values(cluster) 
        for cluster in generate_clusters(base_cluster, 3)]

for i, cluster, marker, color in zip([1, 2, 3],
        three_clusters, ['D','o','*'],['r','g','b']):
    xs, ys = zip(*cluster)
    plt.scatter(xs, ys, color=color, marker=marker)

    x, y = vector_mean(cluster)
    plt.plot(x, y, marker='$' + str(i) + '$', color='black')

plt.title("User locations -- 3 Bottom-Up clusters, Min")
plt.xlabel("blocks east of city center")
plt.ylabel("blocks north of city center")
plt.show()
