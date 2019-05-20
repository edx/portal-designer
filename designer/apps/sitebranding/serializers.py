""" Theming / Site Branding Serializers"""
from rest_framework import serializers
from .models import SiteBranding
from wagtail.wagtailimages.models import Image

class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for Wagtail Images
    """

    class Meta(object):
        model = Image
        read_only = True
        fields = (
            'file'
        )

class SiteBrandingSerializer(serializers.ModelSerializer):
    """
    Serializer for the `SiteBranding` model.
    """
    cover_image = ImageSerializer(many=False, read_only=True)

    class Meta(object):
        model = SiteBranding
        read_only = True
        fields = (
            'program_title',
            'cover_image',
            'banner_border_color',
        )