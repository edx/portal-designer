""" API v1 URLs. """
from django.conf.urls import url, include
from wagtail.api.v2.router import WagtailAPIRouter
from designer.apps.api.v1.views import DesignerPagesAPIEndpoint
from designer.apps.sitebranding.views import SiteBrandingViewSet
from rest_framework.routers import DefaultRouter

wagtail_router = WagtailAPIRouter('content')
wagtail_router.register_endpoint('pages', DesignerPagesAPIEndpoint)

router = DefaultRouter()

# TODO: change to api/v1/site/{sitename}/branding
router.register(r'sitebranding', SiteBrandingViewSet, base_name='sitebranding')

urlpatterns = router.urls
