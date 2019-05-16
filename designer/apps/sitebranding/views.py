""" API for Site Branding """
from .models import SiteBranding
from .serializers import SiteBrandingSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class SiteBrandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ API for SiteBranding model """
    serializer_class = SiteBrandingSerializer
    queryset = SiteBranding.objects.all()
    permission_class = (AllowAny,)

