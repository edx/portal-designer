""" API v1 URLs. """
from django.conf.urls import url
from designer.apps.api.v1.views import DesignerPagesAPIEndpoint, ProgramDetailView

urlpatterns = [
    url(r'^pages/', DesignerPagesAPIEndpoint.as_view(), name="pages"),
    url(r'^programs/', ProgramDetailView.as_view(), name="programs"),
]
