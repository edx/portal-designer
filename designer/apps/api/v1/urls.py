""" API v1 URLs. """
from django.conf.urls import url, include
from wagtail.api.v2.router import WagtailAPIRouter
from designer.apps.api.v1.views import DesignerPagesAPIEndpoint, ProgramDetailView

urlpatterns = [
    url(r'^pages/', DesignerPagesAPIEndpoint.as_view(), name="pages"),
    url(r'^programs/', ProgramDetailView.as_view(), name="programs"),
]
