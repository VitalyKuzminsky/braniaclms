from django.core.management import call_command  # эта штука за нас вызывает python manage.py
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = (
        "This command using for call 'makemessages' with flags:\n"
        "--locale=ru --ignore=venv --no-location"
    )

    def handle(self, *args, **options):
        call_command("makemessages", "--locale=ru", "--ignore=venv", "--no-location")
