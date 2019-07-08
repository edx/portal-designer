""" Serialzers for Page APIs """
from rest_framework import serializers
from wagtail.wagtailcore.models import Page
from designer.apps.pages.models import IndexPage, ProgramPage


class BrandingField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        ret = {
            'cover_image': value.cover_image.file.url,
            'texture_image': value.texture_image.file.url,
            'organization_logo': {
                'url': value.organization_logo_image.file.url,
                'alt': value.organization_logo_alt_text,
            },
            'banner_border_color': value.banner_border_color,
        }
        return ret


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'slug',
            'last_published_at',
        )


class IndexPageBrandingField(BrandingField):
    def to_representation(self, value):
        ret = super(IndexPageBrandingField, self).to_representation(value)
        ret['site_title'] = value.site_title
        return ret


class IndexPageSerializer(serializers.ModelSerializer):

    branding = IndexPageBrandingField(read_only=True, many=True)

    class Meta:
        model = IndexPage
        fields = (
            'id',
            'title',
            'slug',
            'last_published_at',
            'body',
            'branding',
        )


class ProgramPageBrandingField(BrandingField):
    def to_representation(self, value):
        ret = super(ProgramPageBrandingField, self).to_representation(value)
        ret['program_title'] = value.program_title
        return ret


class ProgramPageSerializer(serializers.ModelSerializer):

    branding = ProgramPageBrandingField(read_only=True, many=True)

    class Meta:
        model = ProgramPage
        fields = (
            'id',
            'uuid',
            'title',
            'slug',
            'last_published_at',
            'body',
            'branding',
        )
