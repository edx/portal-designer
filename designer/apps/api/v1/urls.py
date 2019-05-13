""" API v1 URLs. """
from django.conf.urls import url, include
from wagtail.api.v2.router import WagtailAPIRouter
from designer.apps.api.v1.views import DesignerPagesAPIEndpoint

wagtail_router = WagtailAPIRouter('content')
wagtail_router.register_endpoint('pages', DesignerPagesAPIEndpoint)

urlpatterns = [

]
