"""
Root API URLs.

All API URLs should be versioned, so urlpatterns should only
contain namespaces for the active versions of the API.
"""
from django.urls import re_path, include

app_name = 'api'

urlpatterns = [
    re_path(r'^v1/', include(('designer.apps.api.v1.urls', 'v1'))),
]
