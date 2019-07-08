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

# Pages that wagtail creates by default
DEFAULT_WAGTAIL_PAGES = [
    {
        "type": "wagtailcore.Page",
        "last_published_at": None,
        "title": "Root",
        "slug": "root"
    },
    {
        "type": "wagtailcore.Page",
        "last_published_at": None,
        "title": "Welcome to your new Wagtail site!",
        "slug": "home"
    },
]


def create_index_page(site_name):
    """ create index page with test data """
    root_page = Page.get_root_nodes()[0]
    index_page = IndexPage(
        title="{} Index Page".format(site_name),
    )
    root_page.add_child(instance=index_page)
    index_page.save_revision().publish()
    return index_page


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    class Params:
        company_name = factory.LazyAttribute(lambda l: fake.company())

    site_name = factory.LazyAttribute(lambda o: o.company_name)
    hostname = factory.LazyAttribute(
        lambda o: "{company_name}.{domain_name}".format(
            company_name=o.company_name.replace(' ', '-').lower(),
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
        image_title = factory.LazyAttribute(lambda l: ' '.join(fake.words(nb=3)))

    title = factory.LazyAttribute(lambda o: o.image_title)
    file = factory.LazyAttribute(
        lambda o: "original_images/{filename}.{extension}".format(
            filename=o.image_title.replace(' ', '-'),
            extension=fake.file_extension(category='image')
        )
    )
    width = random.randint(100, 10000)
    height = random.randint(100, 10000)
