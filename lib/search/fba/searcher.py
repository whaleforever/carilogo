# import the necessary packages
import numpy as np
import csv
import cv2
import time
from scipy.spatial.distance import braycurtis

class Searcher:

    def __init__(self, indexPath, use_cluster=False):
        # store our index path
        self.indexPath = indexPath
        self.use_cluster = use_cluster

    def chi2_distance(self, histA, histB, eps=1e-10):
        # compute the chi-squared distance
        d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
            for (a, b) in zip(histA, histB)])

        # return the chi-squared distance
        return d

    def intersection(self, histA, histB):
        d = np.sum([np.minimum(a,b) for (a, b) in zip(histA,histB)])
        return d

    def calculate_distance(self, method, histA, histB):
        """ use chi by default """
        if method == "braycurtis":
            return braycurtis(histA, histB)
        elif method == "intersection":
            return self.intersection(histA, histB)
        return self.chi2_distance(histA, histB)

    def search(self, queryFeatures, distance_method="chi", limit=5, cluster_group=None):
        results = {}
        start_time = time.time()
        with open(self.indexPath) as f:
            reader = csv.reader(f)

            for row in reader:
                # parse out the image ID and features, then compute the
                # chi-squared distance between the features in our index
                # and our query features

                if self.use_cluster:
                    features = [float(x) for x in row[2:]]
                    if int(cluster_group)  == int(row[1]):
                        d = self.calculate_distance(distance_method, features, queryFeatures)
                        results[row[0]] = d
                else :
                    features = [float(x) for x in row[1:]]
                    d = self.calculate_distance(distance_method, features, queryFeatures)
                    results[row[0]] = d
        results = sorted([(v, k) for (k, v) in results.items()])
        seconds = time.time() - start_time

        # print result
        # for k,v in results:
        #     print v,k
        # print("--- %s seconds ---" % (seconds))
        if limit is None:
            return seconds, results
        return seconds, results[:limit]
