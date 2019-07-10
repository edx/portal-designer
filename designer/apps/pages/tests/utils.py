# pylint: disable=E1101
""" Page Factories """
import json
from random import randint, getrandbits
from faker import Faker
from faker.providers import lorem, misc, internet
from designer.apps.pages.models import ProgramPage
from designer.apps.core.tests.utils import DocumentFactory

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(internet)


def create_program_page(site, program_title=None):
    """
    Create Program Page for Test Data
    Args:
        site: (Site) site that the program page is under
        program_title: (str) Program Title, one will be auto-generated if not set

    Returns:
        (ProgramPage) Program Page with test data
    """

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

    index_page = site.root_page
    program_title = program_title if program_title else ' '.join([word.capitalize() for word in fake.words(nb=2)])
    program_page = ProgramPage(
        title="{} Program Page".format(program_title),
        uuid=fake.uuid4(),
        program_documents=_create_program_documents(),
        idp_slug=fake.slug(),
    )
    index_page.add_child(instance=program_page)
    program_page.save_revision().publish()
    return program_page
