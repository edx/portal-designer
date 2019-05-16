""" Theming / Site Branding Serializers"""
from rest_framework import serializers
from .models import SiteBranding

class SiteBrandingSerializer(serializers.ModelSerializer):
    """
    Serializer for the `SiteBranding` model.
    """

    class Meta(object):
        model = SiteBranding
        read_only = True
        fields = (
            'program_title',
            'banner_border_color',
        )