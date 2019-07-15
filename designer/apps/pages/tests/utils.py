# pylint: disable=E1101
""" Page Factories """
import json
from random import getrandbits, randint

import factory
from faker import Faker
from faker.providers import internet, lorem, misc

from designer.apps.branding.tests.utils import BrandingFactory
from designer.apps.core.tests.utils import DocumentFactory, SiteFactory
from designer.apps.pages.models import (
    IndexPageBranding,
    ProgramDocuments,
    ProgramPage,
    ProgramPageBranding,
    ProgramHomepage
)

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(internet)


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


class ProgramHomepageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProgramHomepage

    display = factory.LazyAttribute(lambda l: fake.boolean())
    header = factory.LazyAttribute(lambda l: ' '.join([word.capitalize() for word in fake.words(nb=3)]))
    description = factory.LazyAttribute(lambda l: "<ul>{}</ul>".format(
        ["<li>{}</li>".format(s) for s in fake.sentences(nb=4)]
    ))
    link_display_text = factory.LazyAttribute(lambda l: fake.sentence())
    link_url = factory.LazyAttribute(lambda l: fake.url())
    page = factory.LazyAttribute(lambda o: create_program_page(site=SiteFactory()))


def _create_program_documents():
    """
        Create test program documents

        Returns:
            (str) JSON dump of representing a list of program documents
        """
    num_documents = randint(0, 10)

    program_documents = []

    for __ in range(num_documents):

        # randomly make either a link or file type document
        if bool(getrandbits(1)):
            # make a link type doc
            doc = {
                "id": fake.uuid4(),
                "type": "link",
                "value": {
                    "url": fake.url(),
                    "display_text": ' '.join([word.capitalize() for word in fake.words(nb=3)]) + " Link",
                }
            }
        else:
            # make a file type doc
            document_file = DocumentFactory()
            doc = {
                "id": fake.uuid4(),
                "type": "file",
                "value": {
                    "document": document_file.id,
                    "display_text": document_file.title + " File"
                }
            }

        program_documents.append(doc)

    ret = json.dumps(program_documents)
    return ret


class ProgramDocumentsFactory(factory.django.DjangoModelFactory):
    """ Creates an instance of ProgramDocuments for testing """
    class Meta:
        model = ProgramDocuments

    display = factory.LazyAttribute(lambda l: fake.boolean())
    header = factory.LazyAttribute(lambda l: ' '.join([word.capitalize() for word in fake.words(nb=3)]))
    documents = factory.LazyAttribute(lambda l: _create_program_documents())
    page = factory.LazyAttribute(lambda l: create_program_page(site=SiteFactory()))


def create_program_page(site, program_title=None, branding=False, program_documents=False, program_homepage=False):
    """
    Create Program Page for Test Data
    Args:
        site: (Site) site that the program page is under
        program_title: (str) Program Title, one will be auto-generated if not set
        branding: (bool) if True generates branding data for this page
        program_documents: (bool) if True generates program_documents for this page
        program_homepage: (bool) if True generates program_homepage for this page

    Returns:
        (ProgramPage) Program Page with test data
    """
    index_page = site.root_page
    program_title = program_title if program_title else ' '.join([word.capitalize() for word in fake.words(nb=2)])
    program_page = ProgramPage(
        title="{} Program Page".format(program_title),
        uuid=fake.uuid4(),
        idp_slug=fake.slug(),
    )
    index_page.add_child(instance=program_page)
    program_page.save_revision().publish()

    if branding:
        ProgramPageBrandingFactory(site=site, page=program_page)

    if program_documents:
        ProgramDocumentsFactory(page=program_page)

    if program_homepage:
        ProgramHomepageFactory(page=program_page)

    return program_page


def create_branded_site():
    """
    Create a branded Site
    Returns:
        (Site) Site with associated IndexPageBranding
    """
    site = SiteFactory()
    IndexPageBrandingFactory(site=site)
    return site
