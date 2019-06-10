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


def create_index_page(sitename):
    """create_index_page"""
    root_page = Page.get_root_nodes()[0]
    index_page = IndexPage(
        title="{} Index Page".format(sitename),
    )
    root_page.add_child(instance=index_page)
    index_page.save_revision().publish()
    return index_page


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
    root_page = factory.LazyAttribute(
        lambda o: create_index_page(o.site_name)
    )


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

