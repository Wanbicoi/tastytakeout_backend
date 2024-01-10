#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import firebase_admin

from firebase_admin import credentials


cred = credentials.Certificate(
    "utils/tastytakout-firebase-adminsdk-h21ka-1f7dc51960.json"
)

firebase_admin.initialize_app(cred)


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tastytakout.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
