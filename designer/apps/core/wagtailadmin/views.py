from io import StringIO

from django.contrib.auth.decorators import login_required
from django.core import management
from django.http import JsonResponse
from django.template.defaultfilters import linebreaks
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class SiteCreationView(TemplateView):
    """
    View to add new sites from wagtail admin
    """
    template_name = 'wagtailadmin/site_creation.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise PermissionDenied
        return super(SiteCreationView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Runs create_site management command
        """
        sitename = request.POST.get('sitename')
        hostname = request.POST.get('hostname')

        stdout, stderr = StringIO(), StringIO()

        if not (sitename and hostname):
            stderr.write("You must provide a sitename and hostname")

        try:
            management.call_command(
                'create_site',
                '--sitename={}'.format(sitename),
                '--hostname={}'.format(hostname),
                stdout=stdout, stderr=stderr
            )
        except Exception as ex:  # pylint: disable=broad-except
            stderr.write(str(ex))

        return JsonResponse({
            'success_message': linebreaks(stdout.getvalue()),
            'failure_message': linebreaks(stderr.getvalue()),
        })
