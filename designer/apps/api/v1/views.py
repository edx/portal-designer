# Create your views here.
import uuid

from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from wagtail.api.v2.endpoints import PagesAPIEndpoint
from wagtail.api.v2.utils import BadRequestError, page_models_from_string

from designer.apps.api.filters import SiteQueryFilter
from designer.apps.pages.models import ProgramPage

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

class ProgramDetailView(APIView):
    """
        Returns any portal related details for any program passed in through the `programs` query param

        Input:
            ?programs=<uuid_1>,<uuid_2>,<uuid_3>
        Response:
            [] => If not programs specified
            400 => If uuids aren't valid
            404 => If uuids don't exist in application
            List of program detail objects => If all params are valid
    """
    permission_classes = (AllowAny, )

    def get(self, *args, **kwargs):

        requested_programs = self.request.query_params.get('programs')
        if not requested_programs:
            return Response([])
        try:
            program_uuids = [uuid.UUID(program_uuid) for program_uuid in requested_programs.split(',')]
        except ValueError:
            raise serializers.ValidationError('"programs" query param contains malformed UUIDs')

        all_programs = []

        for program_uuid in program_uuids:
            try:
                program_page = ProgramPage.objects.get(uuid=program_uuid)
            except ProgramPage.DoesNotExist:
                raise exceptions.NotFound()

            frontend_url = generate_frontend_url(self.request, program_page)

            all_programs.append({
                'uuid': program_uuid,
                'url': frontend_url,
                'program_name': program_page.title,
            })

        return Response(all_programs)


def generate_frontend_url(request, program_page):
    url = '{scheme}://{hostname}/{slug}'.format(
        scheme='https' if request.is_secure() else 'https',
        hostname=program_page.get_site().hostname,
        slug=program_page.slug
    )
    return url
