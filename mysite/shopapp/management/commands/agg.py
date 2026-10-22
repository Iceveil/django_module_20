

from django.core.management import BaseCommand
from django.db.models import Avg, Min, Max, Count

from shopapp.models import Order, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Start agfregate')
        result = Product.objects.filter(name__contains='smartphone').aggregate(
            Avg('price'),
            Min('price'),
            Max('price'),
            Count('id')
        )
        print(result)
        self.stdout.write(f'Done')