from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext as _


def product_preview_directory_path(instance: "Product", filename: str):
    return "products/product_{pk}/preview/{filename}".format(pk=instance.pk, filename=filename)


def product_image_directory_path(instance: "ProductImage", filename: str):
    return "products/product_{pk}/images/{filename}".format(pk=instance.product.pk, filename=filename)


class Product(models.Model):
    """Модель представляет товары в интернет-магазине
    Заказы тут: :model: 'shopapp.Order'
    """

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.PROTECT,
                                   related_name='products',
                                   default=1)
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)

    def __str__(self) -> str:
        return f'Product(pk={self.pk}, name={self.name!r})'

    def get_absolute_url(self):
        return reverse('shopapp:products_details', kwargs={'pk': self.pk})



class Order(models.Model):

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    delivery_address = models.TextField(blank=True, null=True)
    promocode = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    product = models.ManyToManyField(Product, related_name='orders')
    receipt = models.FileField(null=True, upload_to='orders/receipts')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=product_image_directory_path)