""" Serializers for Page APIs """
from rest_framework import serializers
from wagtail.wagtailcore.models import Page
from designer.apps.pages.models import EnterprisePage, IndexPage, ProgramPage


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
        """
        Get serialized version of branding for the given obj.

        Note:
            This should only be used with a serializer that has a 'branding' field that is being serialized via the
            SerializerMethodField.

        Args:
            obj: (ModelSerializer) The branded page currently being serialized.

        Returns:
            (dict) Serialized version of the branding for the given obj
        """
        branding = obj.branding.first()

        if not branding:
            return {}

        return {
            'cover_image': branding.cover_image.file.url,
            'texture_image': branding.texture_image.file.url,
            'organization_logo': {
                'url': branding.organization_logo_image.file.url,
                'alt': branding.organization_logo_alt_text,
            },
            'banner_border_color': branding.banner_border_color,
        }


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
    external_program_website = serializers.SerializerMethodField()

    class Meta:
        model = ProgramPage
        fields = (
            'id',
            'uuid',
            'title',
            'slug',
            'last_published_at',
            'program_documents',
            'external_program_website',
            'branding',
            'hostname',
        )

    def get_program_documents(self, obj):
        """
        Get serialized version of program_documents for the given obj

        Args:
            obj: (ProgramPage) The program page currently being serialized.

        Returns:
            (dict) Serialized version of the program_documents for the given obj
        """
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

    def get_external_program_website(self, obj):
        """
        Get serialized version of external_program_website for the given obj

        Args:
            obj: (ProgramPage) The program page currently being serialized.

        Returns:
            (dict) Serialized version of the external_program_website for the given obj
        """
        external_program_website = obj.external_program_website.first()

        if not external_program_website:
            return {}

        return {
            'display': external_program_website.display,
            'header': external_program_website.header,
            'description': external_program_website.description,
            'link': {
                'display_text': external_program_website.link_display_text,
                'url': external_program_website.link_url,
            }
        }

    def get_hostname(self, obj):
        """
        Get serialized version of hostname for the given obj

        Args:
            obj: (ProgramPage) The program page currently being serialized.

        Returns:
            (str) Serialized version of the hostname for the given obj
        """
        return obj.get_site().hostname


class EnterprisePageSerializer(BrandedPageSerializerMixin, serializers.ModelSerializer):

    branding = serializers.SerializerMethodField()

    class Meta:
        model = EnterprisePage
        fields = (
            'id',
            'uuid',
            'title',
            'slug',
            'contact_email',
            'last_published_at',
            'branding',
        )
