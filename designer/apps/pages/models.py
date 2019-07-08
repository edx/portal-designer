""" Page models """
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey
from designer.apps.branding.models import Branding
from django.db import models


class IndexPage(Page):
    """
    Used to mark the root of a site

    .. no_pii:
    """
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('branding', label="Index Page Branding", max_num=1),
    ]


class IndexPageBranding(Branding):
    """
    Branding specifically for the Index Page (The site level home page)

    .. no_pii:
    """
    site_title = models.CharField(max_length=128, blank=False, null=True, verbose_name='Site Title')
    page = ParentalKey(IndexPage, on_delete=models.CASCADE, related_name='branding', unique=True)

    panels = [FieldPanel('site_title')] + Branding.panels


class ProgramPage(Page):
    """
    Used to store information for a program on a site

    .. no_pii:
    """
    body = RichTextField(blank=True)
    uuid = models.UUIDField(editable=False, unique=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('branding', label="Program Page Branding", max_num=1),
    ]


class ProgramPageBranding(Branding):
    """
    Branding specifically for the Program Page

    .. no_pii:
    """
    program_title = models.CharField(max_length=128, blank=False, null=True, verbose_name='Program Title')
    page = ParentalKey(ProgramPage, on_delete=models.CASCADE, related_name='branding', unique=True)

    panels = [FieldPanel('program_title')] + Branding.panels
