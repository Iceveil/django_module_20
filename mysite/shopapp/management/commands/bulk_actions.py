from typing import Sequence

from django.core.management import BaseCommand
from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start demo select fields')
        result = Product.objects.filter(name__contains='smartphone',).update(discount=10)
        print(result)

        # info = [
        #     ('smartphone1', 199),
        #     ('smartphone2', 299),
        #     ('smartphone2', 399),
        # ]
        # products = [Product(name=name, price=price) for name, price in info]
        # result = Product.objects.bulk_create(products)
        # for obj in result:
        #     print(obj)
        self.stdout.write(f'Done')