import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'


class Command(BaseCommand):
    """Django command to create owner with owner privileges"""

    # TODO add arg handler
    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)

    def handle(self, username, email, password, *args, **options):
        if username is None:
            username = options['username']
        if email is None:
            username = options['email']
        if password is None:
            password = options['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_owner = False
        user.save()
