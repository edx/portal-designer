""" Page models """
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    StreamFieldPanel,
    RichTextField,
    RichTextFieldPanel,
    MultiFieldPanel,
)
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
    parent_page_types = ['pages.IndexPage']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('uuid', classname="full"),
        FieldPanel('idp_slug'),
        InlinePanel('program_homepage', label="Program Homepage", max_num=1),
        InlinePanel('program_documents', label="Program Documents", max_num=1),
        InlinePanel('branding', label="Program Page Branding", max_num=1),
    ]


class ProgramHomepage(models.Model):
    """
    Section on the Program Page linking back to the Program's Homepage and describing what learners can expect to find
    there.
    For example the program "Masters in Potions Ingredients Science" this section may include a link to the
    "hogwarts.edu" homepage and a description of what learners can expect to find at "hogwarts.edu".  For example,
    "Chat with a professor", "Add or drop a course", "Contact St. Mungo's Poison Control Hotline".
    """
    display = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        verbose_name="Display This Section",
    )
    header = models.CharField(
        max_length=128,
        verbose_name='Header',
        blank=False,
        null=False,
        default='Manage Your Degree'
    )
    description = RichTextField(
        max_length=512,
        verbose_name='description',
        blank=False,
        null=False,
        features=('bold', 'italic', 'ol', 'ul'),
        default="<p>Go to your program's portal to:</p><ul><li>Add or drop courses</li><li>Finance Department</li><li>Contact an advisor</li><li>Get your grade</li><li>Program wide discussions</li><li>and more</li></ul>"
    )
    link_display_text = models.CharField(
        blank=False,
        null=False,
        max_length=128,
        verbose_name="Display Text"
    )
    link_url = models.URLField(
        blank=False,
        null=False,
        verbose_name="URL",
    )

    page = ParentalKey(ProgramPage, on_delete=models.CASCADE, related_name='program_homepage', unique=True)

    panels = [
        FieldPanel('display'),
        FieldPanel('header'),
        RichTextFieldPanel('description'),
        MultiFieldPanel(
            [
                FieldPanel('link_display_text'),
                FieldPanel('link_url'),
            ],
            heading='Link to Homepage',
            classname='collapsible',
        )
    ]


class ProgramDocuments(models.Model):
    """
    List of documents associated with a program

    .. no_pii:
    """
    display = models.BooleanField(
        blank=False,
        null=False,
        default=True,
        verbose_name="Display Program Documents",
    )
    header = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        default="Program Documents",
        verbose_name="Header for Program Documents",
    )
    documents = StreamField(
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
        verbose_name="Documents"
    )

    page = ParentalKey(ProgramPage, on_delete=models.CASCADE, related_name='program_documents', unique=True)

    panels = [
        FieldPanel('display'),
        FieldPanel('header'),
        StreamFieldPanel('documents'),
    ]


class ProgramPageBranding(Branding):
    """
    Branding specifically for the Program Page

    .. no_pii:
    """
    page = ParentalKey(ProgramPage, on_delete=models.CASCADE, related_name='branding', unique=True)
