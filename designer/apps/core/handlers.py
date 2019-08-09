"""
Signal handlers for core app
"""
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from designer.apps.core.models import User


@receiver(post_save, sender=User)
def update_user_groups(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    # TODO: logging, put handlers in submodule (?), create group and permissions via migration
    print('### in update_user_groups, username: ' + str(instance.username) + ', is_staff: ' + str(instance.is_staff))
    if created:
        print('### yep, user was just created')
        if instance.is_staff:
            print('### user is staff, will add to Observers group')
            _add_user_to_observers(instance)
        else:
            print('### user is not staff, nothing to do')
            return
    else:
        print('### nope, user already existed')


def _add_user_to_observers(user):
    observers = Group.objects.get(name='Observers')
    if observers is None:
        print('### oops, could not find group')
        return
    user.groups.add(observers)
    user.save()
