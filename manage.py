#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    if os.environ["DJANGO_ENV"] == "production":
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "vending_machine.config.production.settings"
        )
    else:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "vending_machine.config.development.settings"
        )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )(exc)
    execute_from_command_line(sys.argv)
