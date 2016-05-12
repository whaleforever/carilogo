from django.conf.urls import url, include
from .views import *

urlpatterns = [
    url(r'^fetch-gallery/$', FetchGallery.as_view())
    #url(r'^$', RedirectView.as_view(url="/index.html"))
]
