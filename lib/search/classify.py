import argparse
import csv
from weka.core import serialization, converters, jvm
from weka.core.dataset import Instance
from weka.classifiers import Classifier
from shutil import copyfile


def read_csv_file(file_location):
    data = []
    with open(file_location, 'rb') as csvfile:
        for i, d in enumerate(csv.reader(csvfile)):
            if i > 0:
                data.append(d)
    return data


def assign_classify(file_location, output="classified.out", model="naivebayes.model"):
    data = read_csv_file(file_location)
    jvm.start()
    # load clusters
    obj = serialization.read(model)
    classifier = Classifier(jobject=obj)
    # create file with cluster group
    with open(output, 'w') as cluster_file:
        for index, attrs in enumerate(data):
            inst = Instance.create_instance(attrs[1:])
            pred = classifier.classify_instance(inst)
            print(str(index + 1) + ": label index=" + str(pred))
    jvm.stop()


def query_instance(attributes, model="out.model"):
    """
        get the cluster for defined attributes
        :params attributes: array or list
        :returns: cluster id
    """
    jvm.start()
    # create instance
    inst = Instance(attributes)
    # load model
    obj = serialization.read(model)
    # load cluster and get the cluster_id
    cluster = Clusterer(jobject=obj)
    cluster_id = cluster.cluster_instance(inst)
    jvm.stop()
    return cluster_id


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('file_location', help="arff location")
    ap.add_argument("-o", "--output",
                    default="out.model", help="output model")
    args = ap.parse_args()

    assign_classify(args.file_location)
