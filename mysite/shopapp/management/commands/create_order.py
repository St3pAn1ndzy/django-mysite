from django.contrib.auth.models import User
from django.core.management import BaseCommand

from shopapp.models import Order


class Command(BaseCommand):
    """
    Creates order
    """

    def handle(self, *args, **options):
        self.stdout.write('Creating order')
        user = User.objects.get(username='admin')
        order, created = Order.objects.get_or_create(
            user=user, delivery_address='Ul Pupkina',
            promocode='SALE123')
        self.stdout.write(f'Created order {order}. Result {created}')
