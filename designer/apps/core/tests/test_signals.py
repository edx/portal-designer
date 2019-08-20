""" Tests for Core Signals """

from django.test import TestCase
from django.contrib.auth.models import Group
from django_dynamic_fixture import G
from designer.apps.core.models import User


class PostSaveTests(TestCase):
    """ Tests for the post_save Signal """
    # if a user has proper staff status, logs in for the first time, add them to the group.
    def test_adds_user_to_observers_if_staff(self):
        user = G(User, is_staff=True)
        self.assertEqual(user.is_staff, True)
        self.assertIn(Group.objects.get(name="Observers"), user.groups.all())

    # if a user has no staff status, logs in for the first time, don't add the Observers group
    def test_no_Observer_for_non_staff(self):
        user = G(User, is_staff=False)
        self.assertNotEqual(user.is_staff, True)
        self.assertNotIn(Group.objects.get(name="Observers"), user.groups.all())

    # Only give Observer status to staff on initial login.
    # This is to prove the code that adds the user to the group does not run on
    # every subsequent user save.
    def test_no_Observer_after_initial_creation(self):
        user = G(User, is_staff=False)
        self.assertNotEqual(user.is_staff, True)
        self.assertNotIn(Group.objects.get(name="Observers"), user.groups.all())
        user.is_active = False
        user.save()
        # simulate new login
        user.is_staff = True
        user.is_active = True
        user.save(update_fields=['last_login'])
        self.assertEqual(user.is_staff, True)
        self.assertNotIn(Group.objects.get(name="Observers"), user.groups.all())
