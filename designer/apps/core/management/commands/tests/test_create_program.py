from django.test import TestCase
from django.core.management import call_command, CommandError
from designer.apps.pages.models import ProgramPage
from designer.apps.core.tests.utils import SiteFactory

from faker import Faker
from faker.providers import lorem, company, internet, misc

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(company)
fake.add_provider(internet)
fake.add_provider(misc)


class TestCreateProgramCommand(TestCase):
    """
    Test cases for create_program management command
    """

    def test_site_does_not_exist(self):
        """ Call `create_program` with a site that does not exist, should throw Command Error """
        uuid = fake.uuid4()

        with self.assertRaises(CommandError) as context:
            call_command(
                'create_program',
                '--programname="Test Program"',
                '--hostname="fake.site.com"',
                f"--uuid=\"{uuid}\""
            )

        self.assertTrue('There is no site for hostname ["fake.site.com"]' in str(context.exception))

    def test_happy_path(self):
        """ Successfully Create two Programs and assert that ProgramPages has been properly created """

        # Create site
        site = SiteFactory()
        hostname = site.hostname
        index_page = site.root_page

        program1_name = ' '.join([word.capitalize() for word in fake.words(nb=2)])
        program2_name = ' '.join([word.capitalize() for word in fake.words(nb=2)])

        # Create programs
        call_command(
            'create_program',
            f"--programname={program1_name}",
            f"--hostname={hostname}",
            f"--uuid={fake.uuid4()}",
        )

        call_command(
            'create_program',
            f"--programname={program2_name}",
            f"--hostname={hostname}",
            f"--uuid={fake.uuid4()}",
        )

        # Check that a ProgramPage has been created with the following properties
        programpages = ProgramPage.objects.all()

        self.assertEqual(2, len(programpages), "There should be exactly 2 program pages")

        expected_titles = [name + " Program Page" for name in [program1_name, program2_name]]
        for programpage in programpages:
            # Check the titles of the program pages
            self.assertIn(programpage.title, expected_titles)

            # Check that the program page is a child of site's index page
            self.assertTrue(programpage.is_child_of(index_page))
