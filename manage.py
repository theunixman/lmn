#!/usr/bin/env python
import os
import sys
from data_import.api_connector import scheduler

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lmnop_project.settings")

    scheduler.start()

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

