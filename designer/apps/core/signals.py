""" Signals sent by  Core Models """

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User

# When a new user is created, this signal is actually fired 3 times for 3 seperate sources
# * Once by wagtail
# * Once for the edx_social_auth data
# * Once more to update the last login
# `created` will flip to false after the initial call, but before the edx data (ie: is_staff)
# can be consumed. We cannot rely on it to tell us when the user is first being created.
# Instead, we check to see if `update_fields` exists in kwargs.
# `update_fields` will only exist when the user is already created, and does not exist when
# the data from edx is populated. Essentially, its false for the first 2 steps in the flow,
# but should always exist any time afterwards.
@receiver(post_save, sender=User)
def add_observer_group_to_staff(instance, **kwargs):
    # if the user already exists, just return.
    if kwargs['update_fields']:
        return
    if instance.is_staff:
        observer_group = Group.objects.get(name='Observers')
        instance.groups.add(observer_group)
