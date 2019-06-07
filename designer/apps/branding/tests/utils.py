import factory
from faker import Faker
from faker.providers import color, lorem

from designer.apps.branding.models import Branding
from designer.apps.core.tests.utils import ImageFactory, SiteFactory

fake = Faker()
fake.add_provider(color)
fake.add_provider(lorem)


class SiteBrandingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Branding

    site = factory.SubFactory(SiteFactory)
    cover_image = factory.SubFactory(ImageFactory)
    texture_image = factory.SubFactory(ImageFactory)
    organization_logo_image = factory.SubFactory(ImageFactory)
    organization_logo_alt_text = fake.sentence()
    banner_border_color = fake.safe_hex_color()
