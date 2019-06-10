""" Page models """

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel
from wagtail.api import APIField


class IndexPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('index_page_branding', label="Index Page Branding", max_num=1),
    ]

    api_fields = [
        APIField('index_page_branding'),
    ]


class ProgramPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        InlinePanel('program_page_branding', label="Program Page Branding", max_num=1),
    ]
