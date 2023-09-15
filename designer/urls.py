"""designer URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include(blog_urls))
"""

import os

from auth_backends.urls import oauth2_urlpatterns
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView
from drf_yasg.views import get_schema_view
from edx_api_doc_tools import make_api_info
from rest_framework import permissions
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

from designer.apps.core import views as core_views
from designer.apps.core.wagtailadmin.views import SiteCreationView

admin.autodiscover()


api_info = make_api_info(title="designer API", version="v1")
schema_view = get_schema_view(
    api_info,
    public=False,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = oauth2_urlpatterns + [
    path('api/', include('designer.apps.api.urls')),
    path('api-docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Use the same auth views for all logins, including those originating from the browseable API.
    path('api-auth/', include(oauth2_urlpatterns)),
    path('auto_auth/', core_views.AutoAuth.as_view(), name='auto_auth'),
    path('health/', core_views.health, name='health'),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    path('cms/login/', core_views.wagtail_admin_access_check),
    path('cms/logout/', RedirectView.as_view(url='/logout/')),
    path('cms/sites/new/', SiteCreationView.as_view(), name='create-new-site'),
    path('cms/', include(wagtailadmin_urls)),
    path('', RedirectView.as_view(url='/cms/'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and os.environ.get('ENABLE_DJANGO_TOOLBAR', False):  # pragma: no cover
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
