""" Page models """
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (FieldPanel, InlinePanel,
                                                StreamFieldPanel)
from wagtail.wagtailcore.blocks import CharBlock, StructBlock, URLBlock
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page
from wagtail.wagtaildocs.blocks import DocumentChooserBlock

from designer.apps.branding.models import Branding


class IndexPage(Page):
    """
    Used to mark the root of a site

    .. no_pii:
    """
    parent_page_types = []
    subpage_types = ['pages.ProgramPage']

    content_panels = Page.content_panels + [
        InlinePanel('branding', label="Index Page Branding", max_num=1),
    ]


class IndexPageBranding(Branding):
    """
    Branding specifically for the Index Page (The site level home page)

    .. no_pii:
    """
    page = ParentalKey(IndexPage, on_delete=models.CASCADE, related_name='branding', unique=True)


class ProgramPage(Page):
    """
    Used to store information for a program on a site

    .. no_pii:
    """
    uuid = models.UUIDField(unique=True)
    idp_slug = models.SlugField(max_length=255, verbose_name='IDP Slug', default='')
    program_documents = StreamField(
        [
            ('file', StructBlock(
                [
                    ('display_text', CharBlock()),
                    ('document', DocumentChooserBlock())
                ],
                icon='doc-full'
            )),
            ('link', StructBlock(
                [
                    ('display_text', CharBlock()),
                    ('url', URLBlock()),
                ],
                icon='link'
            ))
        ],
        blank=True,
        verbose_name="Program Documents"
    )

    parent_page_types = ['pages.IndexPage']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('uuid', classname="full"),
        FieldPanel('idp_slug'),
        StreamFieldPanel('program_documents'),
        InlinePanel('branding', label="Program Page Branding", max_num=1),
    ]


class ProgramPageBranding(Branding):
    """
    Branding specifically for the Program Page

    .. no_pii:
    """
    page = ParentalKey(ProgramPage, on_delete=models.CASCADE, related_name='branding', unique=True)
