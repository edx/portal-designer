from django.conf.urls import url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from designer.apps.core.wagtailadmin.views import SiteCreationView


class NewSiteMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.is_staff


@hooks.register('register_settings_menu_item')
def register_new_site_menu_item():
    return NewSiteMenuItem(
        _('Add a Site'),
        urlresolvers.reverse('create-new-site'),
        classnames='icon icon-cogs',
        order=1000
    )


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^create_site/$', SiteCreationView.as_view(), name='create-new-site'),
    ]
