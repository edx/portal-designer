""" Test the Designer Pages API """
from django.test import TestCase
from django.urls import reverse
from wagtail.models import Page

from designer.apps.core.tests.utils import DEFAULT_WAGTAIL_PAGES
from designer.apps.pages.tests.utils import create_program_page, create_site


class TestDesignerPagesAPIEndpoint(TestCase):
    """ Tests for DesignerPagesAPIEndpoint """

    def setUp(self):
        super().setUp()
        self.url = reverse('api:v1:pages')

        # Create a site and associated branding
        self.site = create_site()

        # Create 2 programs under that site and associated branding
        self.program1_page = create_program_page(
            self.site,
            branding=True,
            program_documents=True,
            external_program_website=True
        )
        self.program2_page = create_program_page(
            self.site,
            branding=True,
            program_documents=True,
            external_program_website=True
        )

    @classmethod
    def _get_expected_data(cls, pages, include_default_pages=False):
        """
        Returns a list in the structure of the expected response for the given list of pages
        Args:
            pages: (list) List of IndexPages and ProgramPages
            include_default_pages: (bool) Include the two default pages that wagtail automatically makes

        Returns:
            (list) in the same structure as the expected result.
        """
        expected_data = DEFAULT_WAGTAIL_PAGES if include_default_pages else []

        for page in pages:
            page_type = page._meta.model.__name__
            try:
                page_branding = page.branding.first()
            except AttributeError:
                page_branding = None
            expected_page_data = {
                "type": f"pages.{page_type}",
                "title": page.title,
                "slug": page.slug,
                "last_published_at": Page.objects.get(id=page.id).last_published_at.isoformat().replace('+00:00', 'Z'),
            }
            if page_type != 'IndexPage':
                expected_page_data.update({
                    "branding": {},
                })

                if page_branding:
                    expected_page_data['branding'].update({
                        "organization_logo": {
                            "url": page_branding.organization_logo_image.file.url,
                            "alt": page_branding.organization_logo_alt_text,
                        },
                        "banner_border_color": page_branding.banner_border_color,
                    })
                    cover_image = getattr(page_branding, 'cover_image', None)
                    texture_image = getattr(page_branding, 'texture_image', None)
                    banner_background_color = getattr(page_branding, 'banner_background_color', None)
                    if cover_image:
                        expected_page_data['branding'].update({
                            "cover_image": page_branding.cover_image.file.url,
                        })
                    if texture_image:
                        expected_page_data['branding'].update({
                            "texture_image": page_branding.texture_image.file.url,
                        })
                    if banner_background_color:
                        expected_page_data['branding'].update({
                            "banner_background_color": page_branding.banner_background_color,
                        })

            # Special cases
            if page_type == 'ProgramPage':
                expected_page_data['uuid'] = str(page.uuid)
                expected_page_data['hostname'] = str(page.get_site().hostname)

                program_documents = page.program_documents.first()
                if program_documents:
                    expected_page_data['program_documents'] = {
                        'display': program_documents.display,
                        'header': program_documents.header,
                        'documents': [],
                    }
                    for document in program_documents.documents:
                        if document.block_type == 'link':
                            expected_page_data['program_documents']['documents'].append(
                                {
                                    'display_text': document.value['display_text'],
                                    'url': document.value['url'],
                                }
                            )
                        elif document.block_type == 'file':
                            expected_page_data['program_documents']['documents'].append(
                                {
                                    'display_text': document.value['display_text'],
                                    'document': document.value['document'].file.url,
                                }
                            )
                else:
                    expected_page_data['program_documents'] = {}

                external_program_website = page.external_program_website.first()
                if external_program_website:
                    expected_page_data['external_program_website'] = {
                        'display': external_program_website.display,
                        'header': external_program_website.header,
                        'description': external_program_website.description,
                        'link': {
                            'display_text': external_program_website.link_display_text,
                            'url': external_program_website.link_url,
                        }
                    }
                else:
                    expected_page_data['external_program_website'] = {}

            expected_data.append(expected_page_data)

        return expected_data

    def _assert_correct_response(self, response, expected_data):
        """
        Assert that response is correct.
        Args:
            response: (Response) response from api
            expected_data: (list) expected response data
        """
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(expected_data))

        # making a copy of expected data so that we can safely remove fields once they've been checked
        expected_data = expected_data.copy()

        # sort pages by slug so that we can compare the pages to each other
        expected_data = sorted(expected_data, key=lambda i: i['slug'])
        actual_data = sorted(response.data, key=lambda i: i['slug'])

        for expected_page, actual_page in zip(expected_data, actual_data):

            # Assert that the branding data is the same
            if 'branding' in expected_page:

                if expected_page['branding']:

                    # Assert organization logo is the same
                    self.assertDictEqual(
                        expected_page['branding']['organization_logo'],
                        actual_page['branding']['organization_logo']
                    )

                    # Remove 'organization_logo' we no longer need to check it
                    expected_page['branding'].pop('organization_logo')

                    # Assert that all fields under 'branding' are the same
                    for k in expected_page['branding'].keys():
                        self.assertEqual(expected_page['branding'][k], actual_page['branding'][k])

                else:
                    # Both lists should be empty
                    self.assertEqual(expected_page['branding'], actual_page['branding'])

                # Remove 'branding' from expected_data, we no longer need to check that
                expected_page.pop('branding')

            else:
                self.assertNotIn('branding', actual_page)

            # Assert that the program_document data is the same
            if 'program_documents' in expected_page:

                if expected_page['program_documents']:

                    # Assert that the documents are the same and in the correct order
                    expected_docs = expected_page['program_documents']['documents']
                    actual_docs = actual_page['program_documents']['documents']
                    for expected_doc, actual_doc in zip(expected_docs, actual_docs):
                        self.assertDictEqual(expected_doc, actual_doc)

                    # Remove 'documents' we no longer need to check it
                    expected_page['program_documents'].pop('documents')

                    # Assert that all the other fields under 'program_documents' are the same
                    for k in expected_page['program_documents'].keys():
                        self.assertEqual(
                            expected_page['program_documents'][k],
                            actual_page['program_documents'][k]
                        )

                else:

                    # Both should be empty
                    self.assertEqual(expected_page['program_documents'], actual_page['program_documents'])

                # Remove 'program_documents' we no longer need to check it
                expected_page.pop('program_documents')

            else:
                self.assertNotIn('program_documents', actual_page)

            # Assert the rest of the fields match
            for k in expected_page.keys():
                self.assertEqual(expected_page[k], actual_page[k])

    def test_default_behavior(self):
        """ Verify that all existing pages will be returned when the api is called with no queries. """
        expected_data = self._get_expected_data(
            pages=[
                self.site.root_page,
                self.program1_page,
                self.program2_page,
            ],
            include_default_pages=True,
        )
        response = self.client.get(self.url)
        self._assert_correct_response(response, expected_data)

    def test_specify_hostname(self):
        """ Verify that when the pages api is called with a hostname specified only pages associated with that site are
        returned """
        # Create a second site
        site2 = create_site()
        # Create a number of programs for that site
        site2_program_pages = [create_program_page(site2) for __ in range(3)]

        # Verify that only the pages associated with site2 are in the response
        expected_data = self._get_expected_data([site2.root_page] + site2_program_pages)
        response = self.client.get(self.url, {'hostname': site2.hostname})
        self._assert_correct_response(response, expected_data)

    def test_hostname_does_not_exist(self):
        """ Verify that an empty list is returned when there is no site for the given hostname """
        response = self.client.get(self.url, {'hostname': 'fake.not-real.com'})
        self._assert_correct_response(response, [])

    def test_filter_by_page_type(self):
        """ Verify that when filtering by page type the appropriate pages are returned """
        # Create a second site
        site2 = create_site()
        # Create a number of programs for that site
        site2_program_pages = [create_program_page(site2) for __ in range(3)]

        # Verify that when querying for 'IndexPage's all IndexPages are returned
        expected_data = self._get_expected_data([
            self.site.root_page,
            site2.root_page
        ])
        response = self.client.get(self.url, {'type': 'pages.IndexPage'})
        self._assert_correct_response(response, expected_data)

        # Verify that when querying for 'ProgramPage's all ProgramPages are returned
        expected_data = self._get_expected_data(
            site2_program_pages + [
                self.program1_page,
                self.program2_page
            ]
        )
        response = self.client.get(self.url, {'type': 'pages.ProgramPage'})
        self._assert_correct_response(response, expected_data)
