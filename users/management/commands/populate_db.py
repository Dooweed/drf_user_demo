from django.conf import settings
from django.core.management import BaseCommand

from users.models import User
from users.tests.factories import UserFactory


class Command(BaseCommand):
    """ Command for setting webhook for the bot instance """
    INSTANCES_COUNT = 100

    @staticmethod
    def _generate_superuser():
        User.objects.create_superuser(username='admin', email='admin@example.com', password='123')

    @staticmethod
    def _generate_data():
        UserFactory.create_batch(Command.INSTANCES_COUNT)

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            self._generate_superuser()

        if User.objects.count() < self.INSTANCES_COUNT:
            self._generate_data()
