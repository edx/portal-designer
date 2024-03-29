#!/usr/bin/env python
# pylint: skip-file

"""
Django administration utility.
"""

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "designer.settings.local")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
