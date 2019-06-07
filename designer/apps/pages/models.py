""" Page models """

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel


class BrandedPage(Page):

    content_panels = Page.content_panels + [
        InlinePanel('branded_page', label="Page Branding")
    ]


class IndexPage(BrandedPage):
    body = RichTextField(blank=True)

    content_panels = BrandedPage.content_panels + [
        FieldPanel('body', classname="full"),
    ]


class ProgramPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]
