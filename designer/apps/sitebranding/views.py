""" API for Site Branding """
from .models import SiteBranding
from .serializers import SiteBrandingSerializer
from rest_framework import viewsets
from rest_framework.permissions import AllowAny


class SiteBrandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ API for SiteBranding model """
    serializer_class = SiteBrandingSerializer
    # TODO: change permission class
    permission_class = (AllowAny,)

    def get_queryset(self):
        return SiteBranding.objects.filter(site__hostname=self.kwargs['sitename'])
