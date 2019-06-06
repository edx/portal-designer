""" Create Program management command """
from django.core.management import BaseCommand, CommandError
from django.db import transaction
from wagtail.wagtailcore.models import Site
from designer.apps.pages.models import ProgramPage


class Command(BaseCommand):
    """
     Management command for creating a new program.
     Specifically, this creates a new program page under it's site index page.
     """
    help = "Creates a new program page"

    def add_arguments(self, parser):
        parser.add_argument(
            '--programname',
            help='Name of program',
            required=True
        )
        parser.add_argument(
            '--site',
            help='Hostname of site associated with program',
            required=True
        )

    def create_program_page(self, site, program_name):
        """
        create a program page and make it a child of the site's index page

        Args:
            site: (Site) site that this program is under
            program_name: (str) name of program

        Returns:
            (ProgramPage) home page for the program
        """

        program_page = ProgramPage(
            title="{} Program Page".format(program_name)
        )
        index_page = site.root_page
        index_page.add_child(instance=program_page)
        program_page.save_revision().publish()
        return program_page

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Creates a new program page under the appropriate index page.
        """
        site_hostname = options['site']
        program_name = options['programname']

        try:
            site = Site.objects.get(hostname=site_hostname)
        except Site.DoesNotExist:
            raise CommandError("There is no site for hostname [{}]".format(site_hostname))

        self.create_program_page(site, program_name)
        self.stdout.write('Successfully created program page for "%s"' % program_name)
