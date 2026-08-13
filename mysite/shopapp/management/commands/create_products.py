from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """
    Creates products
    """

    def handle(self, *args, **options):
        self.stdout.write('Creating products')
        products_name = [
            'Laptop',
            'Mouse',
            'Desktop',
        ]
        for name in products_name:
            product, created = Product.objects.get_or_create(name=name)
            self.stdout.write(f'Created product {product.name}')
        self.stdout.write(self.style.SUCCESS('Successfully created products'))
