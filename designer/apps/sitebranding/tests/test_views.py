""" Test Cases for Site Branding Views """
from django.test import TestCase
from .utils import SiteBrandingFactory


class TestSiteBrandingViewSet(TestCase):
    """  Tests for SiteBrandingViewSet  """

    def setUp(self):
        import pudb; pudb.set_trace()
        self.site_branding = SiteBrandingFactory()

    def test_happy_path(self):
        import pudb; pudb.set_trace()
        self.assertFalse(True)
