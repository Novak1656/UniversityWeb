from django.core.management.base import BaseCommand
from decouple import config
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Admin initialization'

    def handle(self, *args, **options):
        username = config('DJANGO_SUPERUSER_USERNAME')
        email = config('DJANGO_SUPERUSER_EMAIL')
        password = config('DJANGO_SUPERUSER_PASSWORD')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password)
            print('Admin has been created.')
        else:
            print('Admin has been initialized.')
