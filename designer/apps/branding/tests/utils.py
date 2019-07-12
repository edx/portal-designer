# pylint: disable=E1101
"""Utilities to enabling testing of Branding related code"""
import factory
from faker import Faker
from faker.providers import color, lorem, company

from designer.apps.branding.models import Branding
from designer.apps.pages.models import IndexPageBranding, ProgramPageBranding
from designer.apps.core.tests.utils import ImageFactory, SiteFactory
from designer.apps.pages.tests.utils import create_program_page

fake = Faker()
fake.add_provider(color)
fake.add_provider(lorem)
fake.add_provider(company)


class BrandingFactory(factory.django.DjangoModelFactory):
    """Creates instance of Branding for testing"""
    class Meta:
        model = Branding

    cover_image = factory.SubFactory(ImageFactory)
    texture_image = factory.SubFactory(ImageFactory)
    organization_logo_image = factory.SubFactory(ImageFactory)
    organization_logo_alt_text = factory.LazyAttribute(lambda l: fake.bs())
    banner_border_color = factory.LazyAttribute(lambda l: fake.safe_hex_color())


class IndexPageBrandingFactory(BrandingFactory):
    """Creates instance of IndexPageBranding for testing"""
    class Meta:
        model = IndexPageBranding

    class Params:
        site = factory.SubFactory(SiteFactory)

    page = factory.LazyAttribute(lambda o: o.site.root_page)


class ProgramPageBrandingFactory(BrandingFactory):
    """Creates instance of ProgramPageBranding for testing"""
    class Meta:
        model = ProgramPageBranding

    class Params:
        site = factory.SubFactory(SiteFactory)

    page = factory.LazyAttribute(lambda o: create_program_page(
        site=o.site,
    ))


def create_branded_site():
    """
    Create a branded Site
    Returns:
        (Site) Site with associated IndexPageBranding
    """
    site = SiteFactory()
    IndexPageBrandingFactory(site=site)
    return site


def create_branded_program_page(site):
    """
    Create a branded program page for the given site

    Args:
        site: (Site) site the program is associated with

    Returns:
        (ProgramPage) ProgramPage that has an associated ProgramPageBranding

    """
    program_page_branding = ProgramPageBrandingFactory(site=site)
    return program_page_branding.page
