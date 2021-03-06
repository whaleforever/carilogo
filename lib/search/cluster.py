import argparse
import csv
from weka.core import serialization, converters, jvm
from weka.core.dataset import Instance
from weka.clusterers import Clusterer
from shutil import copyfile

def check_jvm():
    if not jvm.started:
        jvm.start(max_heap_size="512m")

def create_cluster_model(arff_file, n=10, loader_type="csv", model="kmeans.model"):
    """ create cluster model """
    check_jvm()
    if loader_type == "csv":
        loader = converters.Loader(classname="weka.core.converters.CSVLoader")
    else :
        loader = conventers.Loader(classname="weka.core.converters.ArffLoader")

    data = loader.load_file(arff_file)
    clusterer = Clusterer(
        classname="weka.clusterers.SimpleKMeans", options=["-N", str(n)])
    clusterer.build_clusterer(data)
    serialization.write(model, clusterer)



def read_csv_file(file_location):
    data = []
    with open(file_location, 'rb') as csvfile:
        for i, d in enumerate(csv.reader(csvfile)):
            if i > 0:
                data.append(d)
    return data


def assign_cluster(file_location, file_out="clustered.csv", model="kmeans.model", last_filename=False):
    data = read_csv_file(file_location)
    check_jvm()
    # load clusters
    obj = serialization.read(model)
    clusterer = Clusterer(jobject=obj)

    # create file with cluster group
    with open(file_out, 'w') as output:
        for index, attrs in enumerate(data):
            tmp = []
            if last_filename:
                inst = Instance.create_instance(attrs[:-2])
            else:
                inst = Instance.create_instance(attrs[1:])

            pred = clusterer.cluster_instance(inst)
            dist = clusterer.distribution_for_instance(inst)

            if last_filename :
                tmp.append(attrs[-1])
                tmp.append(pred)
                tmp.extend(attrs[:-2])
            else:
                tmp.append(attrs[0])
                tmp.append(pred)
                tmp.extend(attrs[1:])

            print(str(index + 1) + ": label index=" +
                  str(pred) + ", class distribution=" + str(dist))
            output.write('%s\n'%(','.join(map(str,tmp)) ))


def query_instance(attributes, model="kmeans.model"):
    """
        get the cluster for defined attributes
        :params attributes: array or list
        :returns: cluster id
    """
    check_jvm()
    # create instance
    inst = Instance.create_instance(attributes)
    # load model
    obj = serialization.read(model)
    # load cluster and get the cluster_id
    cluster = Clusterer(jobject=obj)
    cluster_id = cluster.cluster_instance(inst)

    return cluster_id


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('file_location', help="arff location")
    ap.add_argument('--cluster', action="store_true", dest="create_cluster")
    ap.set_defaults(create_cluster=False)
    ap.add_argument("-o", "--output", required=False,
                    default="kmeans.model", help="output model")
    ap.add_argument('--last-filename', action="store_true", dest="last_filename")
    ap.set_defaults(last_filename=False)
    args = ap.parse_args()

    if args.create_cluster:
        create_cluster_model(args.file_location, model=args.output)
    else :
        assign_cluster(args.file_location, model=args.output, last_filename=args.last_filename)
