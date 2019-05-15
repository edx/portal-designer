# Create your views here.

from rest_framework.permissions import AllowAny
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.utils import BadRequestError, page_models_from_string

from designer.apps.api.filters import SiteQueryFilter

class DesignerPagesAPIEndpoint(PagesAPIEndpoint):
    permission_classes = (AllowAny, )
    known_query_parameters = PagesAPIEndpoint.known_query_parameters.union([
        'sitename',
    ])
    filter_backends = [SiteQueryFilter] + PagesAPIEndpoint.filter_backends

    def get_queryset(self):
        '''
            Copied from source and changed the site filtering to be based off
            of query text rather than request.site
        '''
        request = self.request

        # Allow pages to be filtered to a specific type
        try:
            models = page_models_from_string(request.GET.get('type', 'wagtailcore.Page'))
        except (LookupError, ValueError):
            raise BadRequestError("type doesn't exist")

        if not models:
            models = [Page]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = Page.objects.all()

            # Filter pages by specified models
            queryset = filter_page_type(queryset, models)

        # Get live pages that are not in a private section
        queryset = queryset.public().live()

        return queryset
