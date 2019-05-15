from rest_framework.filters import BaseFilterBackend

from wagtail.wagtailcore.models import Site

class SiteQueryFilter(BaseFilterBackend):
    """
    Filters response based on sitename query text
    """
    def filter_queryset(self, request, queryset, view):
        sitename = request.GET.get('sitename')
        if not sitename:
            return queryset
        try:
            site = Site.objects.get(hostname=sitename)
        except Site.DoesNotExist:
            # Return no pages since none match the passed in sitename
            return queryset.none()

        return queryset.descendant_of(site.root_page, inclusive=True)
