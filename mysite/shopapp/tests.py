
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse


#
# class ProductCreateViewTestCase(TestCase):
#     def test_create_product(self):
#         self.user = User.objects.create_user(username='test', password='test')
#         self.user.is_staff = True
#         self.user.save()
#         self.client.force_login(self.user)
#         response = self.client.post(
#             reverse('shopapp:product_form'),
#                 {
#                 'name': 'Table',
#                 'price':'123.45' ,
#                 'description': 'a good',
#                 'discount': '10'
#             }
#         )
#         self.assertRedirects(response, reverse('shopapp:products_list'))


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.credentials = dict(username='test', password='qwerty')
        cls.user = User.objects.create_user(**cls.credentials)
        view_order_perm = Permission.objects.get(
            codename='view_order',
            content_type__app_label='shopapp'
        )
        cls.user.user_permissions.add(view_order_perm)
        cls.user.save()

        from .models import Product
        cls.prod = Product.objects.create(
            name='Softshell',
            description = 'super fabric',
            price = 350,
            discount = 5,
            created_by = cls.user,
        )


    @classmethod
    def tearDownClass(cls):
        cls.prod.delete()
        cls.user.delete()


    def setUp(self):
        self.client.login(**self.credentials)
        response = self.client.post(
            reverse('shopapp:create_order'),
            data={
                'delivery_address': 'Timiryazeva st',
                'product': [str(self.prod.id)],
                'user': [str(self.user.id)],
                'promocode': 'SALE123'
            }
        )
        from .models import Order
        self.new_order = Order.objects.filter(
            delivery_address = 'Timiryazeva st',
            product = self.prod,
            user = self.user
        ).first()

        self.assertIsNotNone(self.new_order)



    def tearDown(self):
        self.new_order.delete()


    def test_order_details(self):
        self.assertEqual(self.new_order.delivery_address, 'Timiryazeva st')
        self.assertIsInstance(self.new_order.promocode, str)

        url = reverse('shopapp:order_details', kwargs={'pk': self.new_order.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        order_from_context = response.context['order']
        self.assertEqual(order_from_context.pk, self.new_order.pk)
