import json
from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from .forms import SearchForm
from lib.search.fba.preprocess import Preprocess
from lib.search.fba.searcher import Searcher


class SearchView(TemplateView):
    template_name="search/index.html"

    def post(self, request, *args, **kwargs):
        image = self.request['file']
        return super(SearchView,self).post(request, *args, **kwargs)
