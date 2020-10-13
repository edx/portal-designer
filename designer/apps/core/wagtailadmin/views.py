from io import StringIO

from django.contrib.auth.decorators import login_required
from django.core import management
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.template.defaultfilters import linebreaks
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class SiteCreationView(TemplateView):
    """
    View to add new sites from wagtail admin
    """
    template_name = 'wagtailadmin/site_creation.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('add_site'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Runs create_site management command
        """
        if not request.user.has_perm('add_site'):
            raise PermissionDenied

        sitename = request.POST.get('sitename')
        hostname = request.POST.get('hostname')

        stdout, stderr = StringIO(), StringIO()

        if not (sitename and hostname):
            stderr.write("You must provide a sitename and hostname")

        try:
            management.call_command(
                'create_site',
                f'--sitename={sitename}',
                f'--hostname={hostname}',
                stdout=stdout, stderr=stderr
            )
        except Exception as ex:  # pylint: disable=broad-except
            stderr.write(str(ex))

        return JsonResponse({
            'success_message': linebreaks(stdout.getvalue()),
            'failure_message': linebreaks(stderr.getvalue()),
        })
