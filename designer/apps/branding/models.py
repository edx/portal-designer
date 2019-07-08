""" Models related to the branding of individual sites """
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from django.db import models
import re
from django.core.exceptions import ValidationError
from modelcluster.models import ClusterableModel


def validate_hexadecimal_color(color):
    """
    Returns true if color is a string in the format hexadecimal format
    ex: '#B62168', '#00a2e4'
    Args:
        color: (str) string representing hexadecimal color

    Returns:
        is_valid_hexadecimal_color: (bool) True if `color` is in valid hexadecimal format
    """
    if re.match(r'#[\dA-Fa-f]{6}', color) is None:
        raise ValidationError("Incorrect format. Must follow hexadecimal format (ex. '#B62168' or '#00a2e4')")


class Branding(models.Model):
    """
    Base Branding model
    """
    cover_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Cover Image'
    )
    texture_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Texture Image'
    )
    organization_logo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Logo Image'
    )
    organization_logo_alt_text = models.CharField(
        max_length=256,
        blank=True,
        null=False,
        default='',
        verbose_name='Logo Alt Text'
    )
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
