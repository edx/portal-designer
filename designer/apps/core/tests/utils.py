# pylint: disable=E1101
"""Utilities to enabling testing of Site related code"""
import random
import factory

from faker import Faker
from faker.providers import company, internet, lorem, misc, person
from wagtail.core.models import Site, Page
from wagtail.images.models import Image
from wagtail.documents.models import Document
from designer.apps.core.models import User

from designer.apps.pages.models import IndexPage

fake = Faker()
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(person)

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


class UserFactory(factory.django.DjangoModelFactory):
    """ Creates instance of User for testing """

    class Meta:
        model = User

    class Params:
        firstname = factory.LazyAttribute(lambda __: fake.first_name())
        lastname = factory.LazyAttribute(lambda __: fake.last_name())

    full_name = factory.LazyAttribute(lambda o: "{firstname} {lastname}".format(
        firstname=o.firstname,
        lastname=o.lastname,
    ))
    first_name = factory.LazyAttribute(lambda o: o.firstname)
    last_name = factory.LazyAttribute(lambda o: o.lastname)
    username = factory.LazyAttribute(lambda o: (o.firstname + o.lastname).lower().replace(' ', ''))
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')
    email = factory.LazyAttribute(lambda __: fake.email())
    is_staff = False
    is_superuser = False


class SiteFactory(factory.django.DjangoModelFactory):
    """Creates instance of Site for testing"""
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
    """Creates instance of Image for testing"""
    class Meta:
        model = Image

    class Params:
        image_title = factory.LazyAttribute(lambda l: ' '.join(fake.words(nb=3)))

    title = factory.LazyAttribute(lambda o: o.image_title)
    file = factory.LazyAttribute(
        lambda o: "/media/original_images/{filename}.{extension}".format(
            filename=o.image_title.replace(' ', '-'),
            extension=fake.file_extension(category='image')
        )
    )
    width = random.randint(100, 10000)
    height = random.randint(100, 10000)


class DocumentFactory(factory.django.DjangoModelFactory):
    """ Creates instance of wagtail Document for testing """

    class Meta:
        model = Document

    class Params:
        doc_title = factory.LazyAttribute(lambda l: ' '.join([word.capitalize() for word in fake.words(nb=3)]))

    title = factory.LazyAttribute(lambda o: o.doc_title)
    file = factory.LazyAttribute(
        lambda o: "/media/documents/{filename}.{extension}".format(
            filename=o.doc_title.replace(' ', '-'),
            extension=fake.file_extension(category='text')
        )
    )
