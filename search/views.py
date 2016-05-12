import json
import cv2
import os
import csv
from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.conf import settings
from django.http import JsonResponse

from .forms import SearchForm
from lib.search.fba.searcher import Searcher
from lib.search.fba.preprocess import Preprocess
from lib.search import cluster
from lib.tools import make_sure_path_exists, handle_uploaded_file


class SearchView(FormView):
    form_class = SearchForm
    template_name = "search/index.html"

    def post(self, request, *args, **kwargs):

        image_file = request.FILES['file']

        try:
            use_cedd = int(request.POST.get('use_cedd', 0))
        except ValueError:
            use_cedd = 0

        if use_cedd:
            RAW_INDEX = "cedd_beverages.csv"
            CLUSTERED_MODEL = "cedd_clusterer.model"
            CLUSTERED_INDEX = "cedd_clustered.csv"
            IMAGE_FOLDER = "sorted"

            query = None
            with open(RAW_INDEX, 'r') as csvfile:
                readers = csv.reader(csvfile)
                for row in readers:
                    if image_file.name == row[-1]:
                        query = row
                        print "got the name"
                        break
            features = query[:-2]
        else:
            CLUSTERED_MODEL = "sorted_kmeans.model"
            CLUSTERED_INDEX = "sorted_clustered.csv"
            IMAGE_FOLDER = "sorted"

            # create tmp_dir
            tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
            make_sure_path_exists(tmp_dir)

            # save tmp file
            tmp_file = os.path.join(tmp_dir, 'tmp.jpg')
            # TODO: will become problem when multiuser access the same page
            handle_uploaded_file(image_file, tmp_file)

            # initialize the image descriptor
            cd = Preprocess((8, 8, 8))
            # load the query image and describe it
            query = cv2.imread(tmp_file)
            features = cd.describe(query)

        searcher = Searcher(CLUSTERED_INDEX, use_cluster=True)
        cluster_group = cluster.query_instance(features, model=CLUSTERED_MODEL)
        seconds, images = searcher.search(
            features, cluster_group=cluster_group, limit=None)

        result = {
            'seconds': seconds,
            'images': ["%s/%s/%s" % (settings.MEDIA_URL, IMAGE_FOLDER, image[1]) for image in images]
        }
        return JsonResponse(result, safe=False)
