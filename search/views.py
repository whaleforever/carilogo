import json
import cv2
import os
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
    template_name="search/index.html"

    def post(self, request, *args, **kwargs):
        # create tmp_dir
        tmp_dir = os.path.join(settings.MEDIA_ROOT, 'tmp')
        make_sure_path_exists(tmp_dir)

        image_file = request.FILES['file']
        # save tmp file
        tmp_file = os.path.join(tmp_dir, 'tmp.jpg')
        #TODO: will become problem when multiuser access the same page
        handle_uploaded_file(image_file, tmp_file)

        # initilalize index
        searcher = Searcher("file_index.csv", use_cluster = True)
        # initialize the image descriptor
        cd = Preprocess((8, 8, 8))

        # load the query image and describe it
        query = cv2.imread(tmp_file)
        features = cd.describe(query)

        searcher = Searcher("clustered.csv", use_cluster = True)
        cluster_group = cluster.query_instance(features)
        seconds, images  = searcher.search(features,cluster_group=cluster_group)

        result = {
            'seconds': seconds,
            'images': [ "%s/%s/%s"%(settings.MEDIA_URL,'sample',image[1]) for image in images ]
        }
        return JsonResponse(result, safe=False)
