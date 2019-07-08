# pylint: disable=E1101
""" Page Factories """
from faker import Faker
from faker.providers import lorem, misc

from designer.apps.pages.models import ProgramPage

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(misc)


def create_program_page(site, program_title=None):
    """
    Create Program Page for Test Data
    Args:
        site: (Site) site that the program page is under
        program_title: (str) Program Title, one will be auto-generated if not set

    Returns:
        (ProgramPage) Program Page with test data
    """
    index_page = site.root_page
    program_title = program_title if program_title else ' '.join([word.capitalize() for word in fake.words(nb=2)])
    program_page = ProgramPage(
        title="{} Program Page".format(program_title),
        body=''.join(["<p>{}</p>".format(p) for p in fake.paragraphs(nb=5)]),
        uuid=fake.uuid4(),
    )
    index_page.add_child(instance=program_page)
    program_page.save_revision().publish()
    return program_page
