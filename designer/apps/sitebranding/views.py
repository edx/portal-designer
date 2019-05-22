""" API for Site Branding """
from .models import SiteBranding
from .serializers import SiteBrandingSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound


class SiteBrandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ API for SiteBranding model """
    serializer_class = SiteBrandingSerializer
    # TODO: change permission class
    permission_class = (AllowAny,)

    def get_queryset(self):
        hostname = self.kwargs['hostname']
        queryset = SiteBranding.objects.filter(site__hostname=hostname)

        if queryset.exists():
            return queryset

        raise NotFound()
