""" API for Site Branding """
from .models import Branding
from .serializers import BrandingSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound


class BrandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ API for SiteBranding model """
    serializer_class = BrandingSerializer
    # TODO: change permission class
    permission_class = (AllowAny,)


