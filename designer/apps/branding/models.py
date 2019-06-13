""" Models related to the branding of individual sites """
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from django.db import models
import re
from django.core.exceptions import ValidationError
from wagtail.api import APIField
from .serializers import ImageField, OrganizationLogoField

def validate_hexadecimal_color(color):
    """
    Returns true if color is a string in the format hexadecimal format
    ex: '#B62168', '#00a2e4'
    Args:
        color: (str) string representing hexadecimal color

    Returns:
        is_valid_hexadecimal_color: (bool) True if `color` is in valid hexadecimal format
    """
    if 7 != len(color):
        raise ValidationError("Incorrect length. Hexadecimal colors must be 7 digits")

    if re.match(r'#[\dA-Fa-f]{6}', color) is None:
        raise ValidationError("Incorrect format. Must follow hexadecimal format (ex. '#B62168')")


class Branding(models.Model):
    # TODO: docstring
    # TODO: squash migrations
    # TODO: check appropriate max length
    # TODO: check that blank should not be false


    # TODO: find better place for program_title
    # TODO: what should go inplace of program title for the hero? page title?
    # program_title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Program Title')
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Cover Image'
    )
    texture_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Texture Image'
    )
    organization_logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Logo Image'
    )
    # TODO: appropriate max length?
    # TODO: blank false appropriate? i think yes
    organization_logo_alt_text = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        default='',
        verbose_name='Logo Alt Text'
    )
    # TODO: ask UX what the default color should be
    # TODO: add verbose name explaining the input
    banner_border_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        default='#FFFFFF',
        validators=[validate_hexadecimal_color],
    )

    panels = [
        ImageChooserPanel('cover_image'),
        ImageChooserPanel('texture_image'),
        MultiFieldPanel(
            [
                ImageChooserPanel('organization_logo_image'),
                FieldPanel('organization_logo_alt_text'),
            ],
            heading='Organization Logo',
            classname='collapsible'
        ),
        FieldPanel('banner_border_color'),
    ]

    api_fields = [
        APIField('cover_image', serializer=ImageField()),
        APIField('texture_image', serializer=ImageField()),
        APIField('organization_logo', serializer=OrganizationLogoField()),
        APIField('banner_border_color'),
    ]