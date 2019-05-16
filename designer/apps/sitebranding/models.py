""" Models related to the branding of individual sites """
from wagtail.contrib.settings.models import BaseSetting, register_setting
from django.db import models


@register_setting
class SiteBranding(BaseSetting):
    # TODO: docstring
    # programTitle: PropTypes.string.isRequired,
    # coverImage: PropTypes.string.isRequired,
    # textureImage: PropTypes.string.isRequired,
    # organizationLogo: PropTypes.shape({
    #     url: PropTypes.string.isRequired,
    #     alt: PropTypes.string,
    # }).isRequired,
    # bannerBorderColor: PropTypes.string,
    # TODO: check appropriate max length
    # TODO: check that blank should not be false
    program_title = models.CharField(max_length=128, blank=False, null=False, verbose_name='Program Title')

