""" Page models """
import uuid

from django.db import models
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.api import APIField
from modelcluster.fields import ParentalKey
from designer.apps.branding.models import Branding
from django.db import models


class IndexPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('branding', label="Index Page Branding", max_num=1),
    ]

    api_fields = [
        APIField('branding'),
    ]


# TODO: should this be with branding?
class IndexPageBranding(Branding):
    """
    Branding specifically for the Index Page (The site level home page)
    """
    # TODO: site title
    page = ParentalKey(IndexPage, on_delete=models.CASCADE, related_name='branding', unique=True)


class ProgramPage(Page):
    body = RichTextField(blank=True)
    uuid = models.UUIDField(editable=False, unique=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('branding', label="Program Page Branding", max_num=1),
    ]

    api_fields = [
        APIField('branding'),
    ]


# TODO: squash migrations
class ProgramPageBranding(Branding):
    """
    Branding specifically for the Program Page
    """
    # TODO: program title
    page = ParentalKey(ProgramPage, on_delete=models.CASCADE, related_name='branding', unique=True)
