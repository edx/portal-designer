# pylint: disable=E1101
""" Test Creation of Pages """
from random import getrandbits, randint

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.text import slugify
from faker import Faker
from faker.providers import color, internet, lorem, misc
from wagtail.wagtailcore.models import Page

from designer.apps.core.tests.utils import (DocumentFactory, ImageFactory,
                                            SiteFactory, UserFactory)
from designer.apps.pages.models import ProgramPage

fake = Faker()
fake.add_provider(misc)
fake.add_provider(internet)
fake.add_provider(lorem)
fake.add_provider(color)


class ProgramPageCreationTests(TestCase):
    """
    Tests for Program Page Creation
    """

    def setUp(self):
        super(ProgramPageCreationTests, self).setUp()

        self.staff_password = fake.password()
        self.staff = UserFactory(is_staff=True, is_superuser=True, password=self.staff_password)
        self.root_page = Page.get_root_nodes()[0]
        self.site = SiteFactory()
        self.site_page = self.site.root_page

    def _create_program_documents(self):
        """
        Create program document data for testing
        """
        doc_count = randint(0, 6)
        ret = {
            'program_documents-TOTAL_FORMS': '1',
            'program_documents-INITIAL_FORMS': '0',
            'program_documents-0-display': True,
            'program_documents-0-header': "{} Documents".format(fake.word().capitalize()),
            'program_documents-0-documents-count': str(doc_count),
        }

        for i in range(doc_count):
            display_text = ' '.join([word.capitalize() for word in fake.words(nb=3)])

            # randomly generate a link or file type document
            if bool(getrandbits(1)):
                # generate a link type document
                ret.update({
                    "program_documents-0-documents-{}-type".format(i): 'link',
                    "program_documents-0-documents-{}-value-url".format(i): fake.url(),
                    "program_documents-0-documents-{}-value-display_text".format(i): "{} Link".format(display_text),
                    "program_documents-0-documents-{}-order".format(i): str(i),
                    "program_documents-0-documents-{}-deleted".format(i): '',
                })

            else:
                # generate a file type document
                ret.update({
                    "program_documents-0-documents-{}-type".format(i): 'file',
                    "program_documents-0-documents-{}-value-document".format(i): DocumentFactory().id,
                    "program_documents-0-documents-{}-value-display_text".format(i): "{} File".format(display_text),
                    "program_documents-0-documents-{}-order".format(i): str(i),
                    "program_documents-0-documents-{}-deleted".format(i): '',
                })

        return ret

    def _create_program_page_data(self, branding=True, program_documents=True, program_homepage=True):
        """
        Generate program page data for testing
        """
        program_name = ' '.join([word.capitalize() for word in fake.words(nb=2)])
        ret = {
            'title': program_name + " Program Page",
            'uuid': fake.uuid4(),
            'idp_slug': fake.slug(),
        }

        if branding:
            ret.update({
                'branding-TOTAL_FORMS': '1',
                'branding-INITIAL_FORMS': '0',
                'branding-0-cover_image': ImageFactory().id,
                'branding-0-texture_image': ImageFactory().id,
                'branding-0-organization_logo_image': ImageFactory().id,
                'branding-0-organization_logo_alt_text': fake.sentence(),
                'branding-0-banner_border_color': fake.safe_hex_color(),
            })
        else:
            ret.update({
                'branding-TOTAL_FORMS': '0',
                'branding-INITIAL_FORMS': '0',
            })

        if program_homepage:
            ret.update({
                'program_homepage-TOTAL_FORMS': '1',
                'program_homepage-INITIAL_FORMS': '0',
                'program_homepage-0-display': True,
                'program_homepage-0-header': ' '.join([word.capitalize() for word in fake.words(nb=3)]),
                'program_homepage-0-description': "<ul>{}</ul>".format(
                    ["<li>{}</li>".format(s) for s in fake.sentences(nb=4)]
                ),
                'program_homepage-0-link_display_text': "Return to {} homepage".format(program_name),
                'program_homepage-0-link_url': fake.url(),
            })
        else:
            ret.update({
                'program_homepage-TOTAL_FORMS': '0',
                'program_homepage-INITIAL_FORMS': '0',
            })

        if program_documents:
            ret.update(self._create_program_documents())
        else:
            ret.update({
                'program_documents-TOTAL_FORMS': '0',
                'program_documents-INITIAL_FORMS': '0',
            })

        return ret

    def _assert_can_create(self, parent, child_model, data):
        """ Assert that a page of type `child_model` can be created with `data` under `parent` """

        assert self.client.login(username=self.staff.username, password=self.staff_password)

        if 'slug' not in data and 'title' in data:
            data['slug'] = slugify(data['title'])
        data['action-publish'] = 'action-publish'

        url = reverse(
            'wagtailadmin_pages:add',
            args=[child_model._meta.app_label, child_model._meta.model_name, parent.pk]
        )
        response = self.client.post(url, data, follow=True)
        if response.status_code != 200:
            if 'form' not in response.context:
                self.fail('Creating page failed unusually')

            form = response.context['form']
            if not form.errors:
                self.fail('Creating a page failed for unknown reason')

            errors = '\n'.join(['  {}:\n    {}'.format(key, '\n'.join(values)) for key, values in form.errors.items()])
            self.fail("Creating a page failed for the following reasons:\n{}".format(errors))

        try:
            child_model.objects.get(slug=data['slug'])
        except child_model.DoesNotExist:
            self.fail("Page not created")

    def test_can_create_program_page(self):
        """ Verify the successful creation of a program page """

        data = self._create_program_page_data()

        self._assert_can_create(self.site_page, ProgramPage, data)

    def test_can_create_simple_program_page(self):
        """ Verify the successful creation of a program page without branding, program_documents or program_homepage """

        data = self._create_program_page_data(branding=False, program_documents=False, program_homepage=False)

        self._assert_can_create(self.site_page, ProgramPage, data)