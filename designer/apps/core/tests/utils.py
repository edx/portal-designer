import factory
import random
from faker import Faker
from faker.providers import company, internet, lorem

from wagtail.wagtailcore.models import Site, Page
from wagtail.wagtailimages.models import Image

from designer.apps.pages.models import IndexPage

fake = Faker()
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(lorem)


class IndexPageFactory(factory.django.DjangoModelFactory):
    """
    Factory For IndexPage (Not to be used for generic Pages, this makes a lot of assumptions)
    """
    class Meta:
        model = IndexPage

    class Params:
        page_title = ' '.join(fake.words(nb=3))

    path = factory.Sequence(lambda n: "0001%04d" % n)
    depth = 2
    numchild = 0
    url_path = factory.LazyAttribute(
        lambda o: "/{}/".format(
            o.page_title.replace(' ', '-')
        )
    )
    title = factory.LazyAttribute(lambda o: o.page_title)


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    class Params:
        site_name = fake.company()

    site_name = factory.LazyAttribute(lambda o: o.site_name)
    hostname = factory.LazyAttribute(
        lambda o: "{company_name}.{domain_name}".format(
            company_name=o.site_name.replace(' ', '-').lower(),
            domain_name=fake.domain_name()
        )
    )
    root_page = factory.SubFactory(IndexPageFactory)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    class Params:
        image_title = ' '.join(fake.words(nb=3))

    # title = factory.SelfAttribute('image_title')
    title = factory.LazyAttribute(lambda o: o.image_title)
    file = factory.LazyAttribute(
        lambda o: "original_images/{filename}.{extension}".format(
            filename=o.image_title.replace(' ', '-'),
            extension=fake.file_extension(category='image')
        )
    )
    width = random.randint(100, 10000)
    height = random.randint(100, 10000)

