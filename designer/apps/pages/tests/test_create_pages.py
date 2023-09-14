""" Test Creation of Pages """
from random import getrandbits, randint

from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from faker import Faker
from faker.providers import color, internet, lorem, misc
from wagtail.models import Page

from designer.apps.core.tests.utils import (DocumentFactory, ImageFactory,
                                            SiteFactory, UserFactory)
from designer.apps.pages.models import EnterprisePage, ProgramPage

fake = Faker()
fake.add_provider(misc)
fake.add_provider(internet)
fake.add_provider(lorem)
fake.add_provider(color)


class PageCreationMixin:
    """
    Mixin for testing page creation
    """

    def setUp(self):
        super().setUp()

        self.staff_password = fake.password()
        self.staff = UserFactory(is_staff=True, is_superuser=True, password=self.staff_password)
        self.root_page = Page.get_root_nodes()[0]
        self.site = SiteFactory()
        self.site_page = self.site.root_page

    def _create_page_data(self, branding=True):
        """
        Generate program page data for testing
        """
        page_name = ' '.join([word.capitalize() for word in fake.words(nb=2)])
        ret = {
            'title': page_name + " Page",
            'uuid': fake.uuid4(),
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

        return page_name, ret

    def _create_program_documents(self):
        """
        Create program document data for testing
        """
        doc_count = randint(0, 6)
        ret = {
            'program_documents-TOTAL_FORMS': '1',
            'program_documents-INITIAL_FORMS': '0',
            'program_documents-0-display': True,
            'program_documents-0-header': f"{fake.word().capitalize()} Documents",
            'program_documents-0-documents-count': str(doc_count),
        }

        for i in range(doc_count):
            display_text = ' '.join([word.capitalize() for word in fake.words(nb=3)])

            # randomly generate a link or file type document
            if bool(getrandbits(1)):
                # generate a link type document
                ret.update({
                    f"program_documents-0-documents-{i}-type": 'link',
                    f"program_documents-0-documents-{i}-value-url": fake.url(),
                    f"program_documents-0-documents-{i}-value-display_text": f"{display_text} Link",
                    f"program_documents-0-documents-{i}-order": str(i),
                    f"program_documents-0-documents-{i}-deleted": '',
                })
            else:
                # generate a file type document
                ret.update({
                    f"program_documents-0-documents-{i}-type": 'file',
                    f"program_documents-0-documents-{i}-value-document": DocumentFactory().id,
                    f"program_documents-0-documents-{i}-value-display_text": f"{display_text} File",
                    f"program_documents-0-documents-{i}-order": str(i),
                    f"program_documents-0-documents-{i}-deleted": '',
                })

        return ret

    def _create_program_page_data(self, branding=True, program_documents=True, external_program_website=True):
        """
        Generate program page data for testing
        """
        page_name, page_data = self._create_page_data(branding=branding)

        if external_program_website:
            page_data.update({
                'external_program_website-TOTAL_FORMS': '1',
                'external_program_website-INITIAL_FORMS': '0',
                'external_program_website-0-display': True,
                'external_program_website-0-header': ' '.join([word.capitalize() for word in fake.words(nb=3)]),
                'external_program_website-0-description': f'<ul>{[f"<li>{s}</li>" for s in fake.sentences(nb=4)]}</ul>',
                'external_program_website-0-link_display_text': f"Return to {page_name} homepage",
                'external_program_website-0-link_url': fake.url(),
            })
        else:
            page_data.update({
                'external_program_website-TOTAL_FORMS': '0',
                'external_program_website-INITIAL_FORMS': '0',
            })

        if program_documents:
            page_data.update(self._create_program_documents())
        else:
            page_data.update({
                'program_documents-TOTAL_FORMS': '0',
                'program_documents-INITIAL_FORMS': '0',
            })

        return page_data

    def _create_enterprise_page_data(self, branding=True, contact_email=True):
        """
        Generate enterprise page data for testing
        """
        _, page_data = self._create_page_data(branding=branding)

        if contact_email:
            page_data.update({
                'contact_email': fake.email(),
            })

        return page_data

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

            errors = '\n'.join(['  {}:\n    {}'.format(
                key, '\n'.join(values)
            ) for key, values in form.errors.items()])
            self.fail(f"Creating a page failed for the following reasons:\n{errors}")

        try:
            child_model.objects.get(slug=data['slug'])
        except child_model.DoesNotExist:
            self.fail("Page not created")

    def _assert_cannot_create(self, parent, child_model, data):
        """
        Assert that a page of type `child_model` cannot be created with `data` under `parent`
        """

        assert self.client.login(username=self.staff.username, password=self.staff_password)

        if 'slug' not in data and 'title' in data:
            data['slug'] = slugify(data['title'])
        data['action-publish'] = 'action-publish'

        url = reverse(
            'wagtailadmin_pages:add',
            args=[child_model._meta.app_label, child_model._meta.model_name, parent.pk]
        )

        self.client.post(url, data, follow=True)

        try:
            child_model.objects.get(slug=data['slug'])
            self.fail("Page was successfully created when it should not have been.")
        except child_model.DoesNotExist:
            pass


class ProgramPageCreationTests(PageCreationMixin, TestCase):
    """
    Tests for Program Page Creation
    """

    def test_can_create_program_page(self):
        """ Verify the successful creation of a program page """

        data = self._create_program_page_data()

        self._assert_can_create(self.site_page, ProgramPage, data)

    def test_can_create_simple_program_page(self):
        """
        Verify the successful creation of a program page without branding, program_documents or external_program_website
        """

        data = self._create_program_page_data(branding=False, program_documents=False, external_program_website=False)

        self._assert_can_create(self.site_page, ProgramPage, data)

    def test_can_create_multiple_program_pages(self):
        """
        Verify the successful creation of multiple program pages.
        """
        first_page_data = self._create_program_page_data()
        second_page_data = self._create_program_page_data()
        self._assert_can_create(self.site_page, ProgramPage, first_page_data)
        self._assert_can_create(self.site_page, ProgramPage, second_page_data)

    def test_cannot_create_program_page(self):
        """
        Verify the unsuccessful creation of a program page when its sibling page(s)
        are of a different type.
        """
        enterprise_page_data = self._create_enterprise_page_data()
        program_page_data = self._create_program_page_data()
        self._assert_can_create(self.site_page, EnterprisePage, enterprise_page_data)
        self._assert_cannot_create(self.site_page, ProgramPage, program_page_data)


class EnterprisePageCreationTests(PageCreationMixin, TestCase):
    """
    Tests for Enterprise Page Creation
    """

    def test_can_create_enterprise_page(self):
        """ Verify the successful creation of a enterprise page """

        data = self._create_enterprise_page_data()

        self._assert_can_create(self.site_page, EnterprisePage, data)

    def test_can_create_simple_enterprise_page(self):
        """
        Verify the successful creation of a enterprise page without branding
        """

        data = self._create_enterprise_page_data(branding=False)

        self._assert_can_create(self.site_page, EnterprisePage, data)

    def test_cannot_create_multiple_enterprise_pages(self):
        """
        Verify the successful creation of multiple enterprise pages.
        """
        first_page_data = self._create_enterprise_page_data()
        second_page_data = self._create_enterprise_page_data()
        self._assert_can_create(self.site_page, EnterprisePage, first_page_data)
        self._assert_cannot_create(self.site_page, EnterprisePage, second_page_data)

    def test_cannot_create_enterprise_page(self):
        """
        Verify the unsuccessful creation of a program page when its sibling page(s)
        are of a different type.
        """
        program_page_data = self._create_program_page_data()
        enterprise_page_data = self._create_enterprise_page_data()
        self._assert_can_create(self.site_page, ProgramPage, program_page_data)
        self._assert_cannot_create(self.site_page, EnterprisePage, enterprise_page_data)
