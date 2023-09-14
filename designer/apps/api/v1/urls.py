""" API v1 URLs. """
from django.urls import re_path
from designer.apps.api.v1.views import DesignerPagesAPIEndpoint, ProgramDetailView

urlpatterns = [
    re_path(r'^pages/', DesignerPagesAPIEndpoint.as_view(), name="pages"),
    re_path(r'^programs/', ProgramDetailView.as_view(), name="programs"),
]
