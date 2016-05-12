import argparse
import os
import cv2
import connector
import settings
import cluster
from shutil import copyfile
from fba.preprocess import Preprocess
from fba.searcher import Searcher


def create_database():
    if not os.path.isfile(settings.DATABASE):
        connector.initial(table="image", feature="text",
                          cluster="int", weka_id="int", image_path="text")


def initialize():
    #TODO: need to fix database indexing
    # create_database()
    # index.indexing('images/ori_data', using="db")
    index.indexing('images/ori_data', using='file')
    # create cluster
    # cluster.create_cluster_model()


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--index", required=True,
                    help="Path to where the computed index will be stored")
    ap.add_argument("-q", "--query", required=True,
                    help="Path to the query image")
    ap.add_argument("-r", "--result-path", required=True,
                    help="Path to the result path")
    ap.add_argument("--cluster", action='store_true')
    args = vars(ap.parse_args())

    # initialize the image descriptor
    cd = Preprocess((8, 8, 8))

    # load the query image and describe it
    query = cv2.imread(args["query"])
    features = cd.describe(query)

    if args["cluster"]:
        searcher = Searcher(args["index"], use_cluster = True)
        cluster_group = cluster.query_instance(features)
        results  = searcher.search(features,cluster_group=cluster_group)
    else:

        # perform the search
        searcher = Searcher(args["index"])
        results = searcher.search(features)

    # display the query
    cv2.namedWindow("Query", cv2.WINDOW_NORMAL)
    cv2.imshow("Query", query)
    cv2.resizeWindow("Query", 800, 600)

    if not results:
        print "No result ..."
    else :
        print "Total Results",len(results)
    # loop over the results
    for (score, resultID) in results:
        copyfile(args["result_path"] + "/" + resultID, 'result/' + resultID)
        # load the result image and display it
        result = cv2.imread(args["result_path"] + "/" + resultID)
        cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
        cv2.imshow("Result", result)
        cv2.resizeWindow("Result", 800, 600)
        cv2.waitKey(0)
