from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        product_values = Product.objects.values('pk', 'name')
        for p_value in product_values:
            print(p_value)
        self.stdout.write(f'Done')