""" Models related to the branding of individual sites """
from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.models import Image
from designer.apps.branding.utils import validate_hexadecimal_color


class Branding(models.Model):
    """
    Base Branding model

    .. no_pii:
    """
    organization_logo_image = models.ForeignKey(
        Image,
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
        MultiFieldPanel(
            [
                FieldPanel('organization_logo_image'),
                FieldPanel('organization_logo_alt_text'),
            ],
            heading='Organization Logo',
            classname='collapsible'
        ),
        FieldPanel('banner_border_color'),
    ]
