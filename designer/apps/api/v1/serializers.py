""" Serializers for Page APIs """
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


class IndexPageSerializer(serializers.ModelSerializer):

    branding = BrandingField(read_only=True, many=True)

    class Meta:
        model = IndexPage
        fields = (
            'id',
            'title',
            'slug',
            'last_published_at',
            'branding',
        )


class ProgramDocumentField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        if value.block_type == 'link':
            ret = {
                'display_text': value.value['display_text'],
                'url': value.value['url'],
            }
        elif value.block_type == 'file':
            ret = {
                'display_text': value.value['display_text'],
                'document': value.value['document'].file.url,
            }
        else:
            raise ValueError("[{}] is not a valid block_type for a ProgramDocument")

        return ret


class ProgramPageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Program Page
    """
    program_documents = ProgramDocumentField(read_only=True, many=True)
    branding = BrandingField(read_only=True, many=True)
    hostname = serializers.SerializerMethodField()

    class Meta:
        model = ProgramPage
        fields = (
            'id',
            'uuid',
            'title',
            'slug',
            'last_published_at',
            'program_documents',
            'branding',
            'hostname',
            'idp_slug',
        )

    def get_hostname(self, obj):
        return obj.get_site().hostname
