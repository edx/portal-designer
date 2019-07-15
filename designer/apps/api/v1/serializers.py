""" Serializers for Page APIs """
from rest_framework import serializers
from wagtail.wagtailcore.models import Page
from designer.apps.pages.models import IndexPage, ProgramPage


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = (
            'id',
            'title',
            'slug',
            'last_published_at',
        )


class BrandedPageSerializerMixin(object):
    def get_branding(self, obj):
        branding = obj.branding.first()

        if not branding:
            return {}

        ret = {
            'cover_image': branding.cover_image.file.url,
            'texture_image': branding.texture_image.file.url,
            'organization_logo': {
                'url': branding.organization_logo_image.file.url,
                'alt': branding.organization_logo_alt_text,
            },
            'banner_border_color': branding.banner_border_color,
        }
        return ret


class IndexPageSerializer(BrandedPageSerializerMixin, serializers.ModelSerializer):

    branding = serializers.SerializerMethodField()

    class Meta:
        model = IndexPage
        fields = (
            'id',
            'title',
            'slug',
            'last_published_at',
            'branding',
        )


class ProgramPageSerializer(BrandedPageSerializerMixin, serializers.ModelSerializer):
    """
    Serializer for the Program Page
    """
    program_documents = serializers.SerializerMethodField()
    branding = serializers.SerializerMethodField()
    hostname = serializers.SerializerMethodField()
    program_homepage = serializers.SerializerMethodField()

    class Meta:
        model = ProgramPage
        fields = (
            'id',
            'uuid',
            'title',
            'slug',
            'last_published_at',
            'program_documents',
            'program_homepage',
            'branding',
            'hostname',
            'idp_slug',
        )

    def get_program_documents(self, obj):
        program_documents = obj.program_documents.first()

        if not program_documents:
            return {}

        ret = {
            'display': program_documents.display,
            'header': program_documents.header,
            'documents': [],
        }
        for document in program_documents.documents:
            if document.block_type == 'link':
                ret['documents'].append({
                    'display_text': document.value['display_text'],
                    'url': document.value['url'],
                })
            elif document.block_type == 'file':
                ret['documents'].append({
                    'display_text': document.value['display_text'],
                    'document': document.value['document'].file.url,
                })
            else:
                raise ValueError("[{}] is not a valid block_type for a ProgramDocument")

        return ret


    def get_program_homepage(self, obj):
        program_homepage = obj.program_homepage.first()

        if not program_homepage:
            return {}

        ret = {
            'display': program_homepage.display,
            'header': program_homepage.header,
            'description': program_homepage.description,
            'link': {
                'display_text': program_homepage.link_display_text,
                'url': program_homepage.link_url,
            }
        }
        return ret


    def get_hostname(self, obj):
        return obj.get_site().hostname
