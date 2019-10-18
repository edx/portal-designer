# pylint: disable=E1101
"""Utilities to enabling testing of Branding related code"""
import factory
from faker import Faker
from faker.providers import color, lorem, company

from designer.apps.branding.models import Branding
from designer.apps.core.tests.utils import ImageFactory

fake = Faker()
fake.add_provider(color)
fake.add_provider(lorem)
fake.add_provider(company)


class BrandingFactory(factory.django.DjangoModelFactory):
    """Creates instance of Branding for testing"""
    class Meta:
        model = Branding

    organization_logo_image = factory.SubFactory(ImageFactory)
    organization_logo_alt_text = factory.LazyAttribute(lambda l: fake.bs())
    banner_border_color = factory.LazyAttribute(lambda l: fake.safe_hex_color())
