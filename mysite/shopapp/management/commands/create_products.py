from django.core.management import BaseCommand

from shopapp.models import Product


class Command(BaseCommand):
    """Create products"""

    def handle(self, *args, **options):
        self.stdout.write('Create products')
        product_names = ['Oxford', 'Dewspo', 'Biflex']
        for name in product_names:
            product, created = Product.objects.get_or_create(name=name)
            self.stdout.write(f'Created {product} at {created}')
        self.stdout.write(self.style.SUCCESS('Products created'))