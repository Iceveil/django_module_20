from typing import Sequence

from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Model
from django.db import transaction

from shopapp.models import Order, Product


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Create command!')
        user = User.objects.get(username='admin')
        products: Sequence[Product] = Product.objects.all()
        order, created = Order.objects.get_or_create(
            delivery_address = 'Abbey Road St. 33',
            promocode = 'BEATLES 37',
            user=user
        )

        for prod in products:
            order.product.add(prod)
        order.save()
        self.stdout.write(f'Created order {order}')