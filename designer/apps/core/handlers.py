"""
Signal handlers for core app
"""
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from designer.apps.core.models import User

OBSERVERS = 'Observers'


@receiver(post_save, sender=User)
def update_user_groups(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    # TODO: logging, put handlers in submodule (?), create group and permissions via migration, add doc, is there a
    # better way to check "is created or just had is_staff set to true"? if we remove staff, do we need to remove
    # from Observers?
    print('### in update_user_groups, username: ' + str(instance.username) + ', is_staff: ' + str(instance.is_staff))

    if instance.is_staff and not instance.groups.filter(name=OBSERVERS).exists():
        print('### user is staff but not in group, will add to Observers group')
        observers = Group.objects.get(name=OBSERVERS)
        if observers is None:
            print('### oops, could not find group')
            return
        instance.groups.add(observers)
        instance.save()
    else:
        print('### user is not staff or user was already in the group, nothing to do')
