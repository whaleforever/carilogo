# import the necessary packages
import argparse
import glob
import cv2
import re
from fba.preprocess import Preprocess


def extract_feature(db_dir, output=None, bins=(8,12,3), training=False):
    # initialize the color descriptor
    cd = Preprocess(bins)
    content = ""
    feature_length = 0
    # create the header
    labels = ['african', 'beach', 'building', 'bus', 'dinosaur', 'elephant',
                   'flower', 'horse', 'mountain', 'food']
    # use glob to grab the image paths and loop over them
    for imagePath in glob.glob(db_dir + "/*"):
        # extract the image ID (i.e. the unique filename) from the image
        # path and load the image itself
        imageID = imagePath[imagePath.rfind("/") + 1:]
        image = cv2.imread(imagePath)

        # describe the image
        features = cd.describe(image)
        # write the features to file
        features = [str(f) for f in features]
        #calculate how many features
        if not feature_length :
            feature_length = len(features)

        if training:
            #TODO: need to fix this hack, for labeling
            num = re.match(r'(\d+)', imageID).group()
            key = int(num) / 100
            content +="\"%s\",%s\n" % (labels[key], ",".join(features))
        else:
            content +="\"%s\",%s\n" % (imageID, ",".join(features))

    if training :
        header = "label,%s\n"%','.join([str(a) for a in range(feature_length)])
        output.write(header)
    output.write(content)


def indexing(db_dir, using=None, filename='file_index.csv'):
    if using == "file":
        # open the output index file for writing
        output = open(filename, "w")
        extract_feature(db_dir, output, bins=(8,8,8))
        # close the index file
        output.close()
    else:
        extract_feature(db_dir)


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dataset", required=True,
                    help="Path to the directory that contains the images to be indexed")
    ap.add_argument("-i", "--index", required=True,
                    help="Path to where the computed index will be stored")
    ap.add_argument("-t", "--training", default=False)
    args = vars(ap.parse_args())
    indexing(args['dataset'], using="file", filename=args['index'])
