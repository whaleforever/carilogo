from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import SearchForm


class SearchView(FormView):
    form_class = SearchForm
    template_name="search/index.html"

    def form_valid(self, form):
        print "this is valid"
        return super(SearchView, self).form_valid(form)
