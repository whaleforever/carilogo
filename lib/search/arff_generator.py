import argparse
import os
import cv2
import arff
import re


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def extract_hist(image_path, bins=[8, 8, 8]):
    image = cv2.imread(image_path)
    # preprocess
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # extract histogram
    hist = cv2.calcHist([image], [0, 1, 2], None,
                        bins, [0, 180, 0, 256, 0, 256])
    # hist = cv2.normalize(hist,hist)
    return hist.flatten()


def generate_arff(label_list, split_by, datadir, output_file='out.arff', print_name=False):
    # images = [ f for f in ["313.jpg","435.jpg","600.jpg"] if os.path.isfile(os.path.join(datadir,f))]
    # images = [f for f in os.listdir(datadir) if f not in [
        # "313.jpg", "435.jpg", "600.jpg"] and os.path.isfile(os.path.join(datadir, f))]

    # list all images from datadir
    images = [ f for f in os.listdir(datadir) if os.path.isfile(os.path.join(datadir,f)) and f ]
    images = natural_sort(images)
    obj = {
        'relation': 'photo',
        'attributes': [
            ('label', label_list)
        ],
        'data': []
    }

    if print_name :
        obj['attributes'].insert(0,('name', 'STRING'))
    for i in range(0, 512):
        obj['attributes'].append(("%s" % i, 'REAL'))
    key = 0

    for c, image in enumerate(images):
        path = os.path.join(datadir, image)
        # extracted feature
        features = extract_hist(path)

        num = re.match(r'(\d+)', image).group()
        key = int(num) / 100

        if print_name:
            temp = [image, label_list[key]]
        else :
            temp = [label_list[key]]
        temp.extend(features)
        obj['data'].append(temp)
    with open(output_file, 'w') as o:
        arff.dump(obj, o)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--path", required=True,
                    help="Path to directory where file is stored")
    ap.add_argument("-o", "--output", help="output of arrf file ")
    args = vars(ap.parse_args())

    output = args.get("output", "train.arff")

    curdir = os.path.dirname(os.path.abspath(__file__))
    datadir = args["path"]
    generate_arff(['african', 'beach', 'building', 'bus', 'dinosaur', 'elephant',
                   'flower', 'horse', 'mountain', 'food'], 100, datadir, output_file=output, print_name=False)
