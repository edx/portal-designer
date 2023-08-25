"""Create Site management command"""
import re

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Page, Site, Collection, GroupPagePermission, GroupCollectionPermission

from designer.apps.pages.models import IndexPage


MODERATOR_PERMISSIONS = {
    'page_permissions': ['add', 'edit', 'publish'],
    'collection_permissions': [
        'add_image', 'change_image', 'delete_image',
        'add_document', 'change_document', 'delete_document',
    ],
    'core_permissions': ['access_admin']
}


class Command(BaseCommand):
    """ Management command for creating new site, complete with site-specific user groups"""
    help = "Creates a new site and user group"

    def add_arguments(self, parser):
        parser.add_argument(
            '--sitename',
            help='Name of site',
            required=True
        )
        parser.add_argument(
            '--hostname',
            help='Hostname of new site',
            required=True
        )

    def create_index_page(self, sitename):
        """create_index_page"""
        root_page = Page.get_root_nodes()[0]
        index_page = IndexPage(
            title=f"{sitename} Index Page",
        )
        root_page.add_child(instance=index_page)
        index_page.save_revision().publish()
        return index_page

    def create_collection(self, name):
        """create_collection"""
        root_collection = Collection.get_first_root_node()
        collection = Collection(
            name=name
        )
        root_collection.add_child(instance=collection)
        return collection

    def add_group_permissions_by_codename(self, group, codename, page=None, collection=None):
        """
            Adds all permissions to groups based on PERMISSIONS dict above.
            Params:
                group : (Group) Group to add permissions to
                codename: (str) Name of permissions to assign
                page: (Page) Root page to give permission to (if provided)
                collection: (Collection) Collection to give group access to (if provided)

            NOTE: GroupPagePermission model takes a permission_type string instead of an actual permission. For
            simplicity, we are using the same `codename` field for this data even through it is not the `codename`
            field on a Permission model.
        """
        if page:
            GroupPagePermission.objects.create(
                group=group,
                page=page,
                permission_type=codename
            )
        elif collection:
            permission = Permission.objects.get(codename=codename)
            GroupCollectionPermission.objects.create(
                group=group,
                collection=collection,
                permission=permission
            )
        else:
            permission = Permission.objects.get(codename=codename)
            group.permissions.add(permission)

    def create_groups_and_permissions(self, name, index_page, collection):
        group = Group.objects.create(
            name=f'{name}_Moderators'
        )

        for codename in MODERATOR_PERMISSIONS['page_permissions']:
            self.add_group_permissions_by_codename(group, codename, page=index_page)
        for codename in MODERATOR_PERMISSIONS['collection_permissions']:
            self.add_group_permissions_by_codename(group, codename, collection=collection)
        for codename in MODERATOR_PERMISSIONS['core_permissions']:
            self.add_group_permissions_by_codename(group, codename)

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Creates a new Site complete with:
            - site
            - index page
            - collection for images
            - groups & permissions (collection names, root page, title)
        """
        sitename = options['sitename']
        hostname = options['hostname']

        valid_hostname = re.compile(r'^[a-zA-Z0-9.\-]*$')
        if not valid_hostname.match(hostname):
            raise CommandError("Invalid hostname. Hostname should consist of letters, numbers, periods, and hyphens")

        index_page = self.create_index_page(sitename)
        site = Site.objects.create(
            hostname=hostname,
            port=80,
            root_page=index_page,
            site_name=sitename,
            is_default_site=False,
        )
        collection = self.create_collection(sitename)
        self.create_groups_and_permissions(
            sitename,
            index_page=index_page,
            collection=collection,
        )

        self.stdout.write('Successfully created site "%s"' % sitename)
