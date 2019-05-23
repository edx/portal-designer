import factory

from designer.apps.sitebranding.models import SiteBranding

from wagtail.wagtailcore.models import Site


class SiteFactory(factory.Factory):
    class Meta:
        model = Site



class SiteBrandingFactory(factory.Factory):
    class Meta:
        model = SiteBranding