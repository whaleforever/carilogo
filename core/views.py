from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.conf import settings


class StaticRedirectView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return "%s%s" % (settings.STATIC_URL, self.request.path)


class AngularRedirectView(RedirectView):

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        return "%s%s" % (settings.ANGULAR_URL, self.request.path)
