"""
API view module
"""
import uuid

from rest_framework import exceptions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from wagtail.api.v2.utils import BadRequestError, page_models_from_string
from wagtail.models import Page, Site

from designer.apps.pages.models import ProgramPage
from .serializers import PageSerializer, IndexPageSerializer, ProgramPageSerializer, EnterprisePageSerializer


PAGE_TYPE_SERIALIZERS = {
    'pages.IndexPage': IndexPageSerializer,
    'pages.ProgramPage': ProgramPageSerializer,
    'pages.EnterprisePage': EnterprisePageSerializer,
}


class DesignerPagesAPIEndpoint(APIView):
    """
    Returns all pages and all their data. Can be filtered by page type and hostname via querystring.
    """
    # Note: Wagtail's page API didn't allow for retrieval of full details of multiple
    # models and the effort to overwrite it was greater than to write a simple API.
    # The code below is heavily influenced by the Wagtail API.
    # permission_classes = (AllowAny, )

    # Allow pages to be filtered to a specific type
    def get_queryset(self):
        """Allows the user to 1+ Page-derived models to query"""
        try:
            models = page_models_from_string(self.request.GET.get('type', 'wagtailcore.Page'))
        except (LookupError, ValueError) as exception:
            raise BadRequestError("type doesn't exist") from exception

        if not models:
            models = [Page]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = Page.objects.select_related('site').all()

            # Filter pages by specified models
            queryset = self._filter_page_type(queryset, models)

        queryset = queryset.public().live().specific()
        return queryset

    def get(self, request):
        """Returns a list of Page-derived objects, filtered by hostname"""
        hostname = self.request.query_params.get('hostname')
        queryset = self.get_queryset()
        if hostname:
            queryset = self.filter_by_hostname(queryset, hostname)

        pages = self._get_serialized_pages(queryset)

        return Response(pages)

    @staticmethod
    def _filter_page_type(queryset, page_models):
        """
        Filter pages by specified models
        """
        qs = queryset.none()

        for model in page_models:
            qs |= queryset.type(model)

        return qs

    @staticmethod
    def _get_serialized_pages(queryset):
        """
        Get serialized data for pages in queryset
        Args:
            queryset: (Queryset) of Pages

        Returns:
            (list) of serialized (dict) data for each page in the queryset
        """
        pages = []
        for page in queryset:
            page_type = f'{page._meta.app_label}.{page._meta.model.__name__}'

            if page_type in PAGE_TYPE_SERIALIZERS:
                serialized_data = PAGE_TYPE_SERIALIZERS[page_type](page).data

            else:
                serialized_data = PageSerializer(page).data

            serialized_data['type'] = page_type
            pages.append(serialized_data)

        return pages

    def filter_by_hostname(self, queryset, hostname):
        """Filters a queryset by the hostname of the site it's attached to"""
        try:
            site = Site.objects.get(hostname=hostname)
        except Site.DoesNotExist:
            # Return no pages since none match the passed in hostname
            return queryset.none()
        return queryset.descendant_of(site.root_page, inclusive=True)


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
        """Returns program details with 'programs' query param"""
        requested_programs = self.request.query_params.get('programs')
        if not requested_programs:
            return Response([])
        try:
            program_uuids = [uuid.UUID(program_uuid) for program_uuid in requested_programs.split(',')]
        except ValueError as exception:
            raise serializers.ValidationError('"programs" query param contains malformed UUIDs') from exception

        all_programs = []

        for program_uuid in program_uuids:
            try:
                program_page = ProgramPage.objects.get(uuid=program_uuid)
            except ProgramPage.DoesNotExist as exception:
                raise exceptions.NotFound() from exception

            frontend_url = generate_frontend_url(self.request, program_page)

            all_programs.append({
                'uuid': program_uuid,
                'url': frontend_url,
                'program_name': program_page.title,
            })

        return Response(all_programs)


def generate_frontend_url(request, program_page):
    """Used to create the frontend URL based on the program page data"""
    scheme = 'https' if request.is_secure() else 'http'
    hostname = program_page.get_site().hostname
    slug = program_page.slug
    return f'{scheme}://{hostname}/{slug}'
