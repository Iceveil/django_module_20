import json
from csv import DictWriter
from multiprocessing import context

from django.contrib.auth.models import Group, User
from django.db.migrations import writer
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache

from timeit import default_timer
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action, parser_classes
from rest_framework.request import Request
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.syndication.views import Feed

import logging

from .models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm, GroupForm
from .serializers import ProductSerializer, OrderSerializer
from .common import save_csv_products


logger = logging.getLogger(__name__)


class LatestProductsFeed(Feed):
    title = "Shopapp — последние товары"
    description = "Свежие поступления в интернет-магазине Shopapp"
    link = reverse_lazy('shopapp:products_list')

    def items(self):
        return Product.objects.filter(created_at__isnull=False).order_by("-created_at")[:5]

    def item_title(self, item: Product):
        return item.name

    def item_description(self, item: Product):
        return item.description[:200]

    def item_link(self, item: Product):
        return reverse('shopapp:products_details', kwargs=({'pk': item.pk}))



@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =  [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description',]
    filterset_fields = [
        'name',
        'description',
        'price',
        'discount',
        'created_at',
        'archived',
    ]
    ordering_fields = [
        'name',
        'description',
        'price',
    ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, returns 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type="text/csv")
        filename = 'products-export.csv'
        response["Content-Disposition"] = f"attachment; filename={filename}-export.csv"
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow(
                {
                    field: getattr(product, field)
                    for field in fields
                }
            )
        return response

    @action(
        detail=False,
        methods=['post'],
        parser_classes=[MultiPartParser,]
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['file'].file,
            encoding=request.encoding,
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @method_decorator(cache_page(60))
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['product', 'user']
    filterset_fields = [
        'user',
        'product',
        'created_at',
        'delivery_address',
    ]
    ordering_fields = [
        'user',
        'product',
        'created_at',
    ]


class ShopAppView(View):
    def get(self, request: HttpRequest) -> HttpResponse:

        products = [
            ('Oxford', 50),
            ('Biflex', 200),
            ('Dewspo', 100)
        ]
        orders = [
            ('oxford', 10000),
            ('biflex', 2000),
            ('dewspo', 40000)
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
            'orders': orders
        }
        print('context', context)
        return render(request, 'shopapp/shop-index.html', context=context)


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm,
            'groups': Group.objects.prefetch_related('permissions').all()
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = "shopapp/products-details.html"
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'

class ProductsListView(ListView):
    template_name = "shopapp/products-list.html"
    model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class OrdersListView(LoginRequiredMixin,ListView):
    queryset = Order.objects.select_related('user').prefetch_related('product')


class OrderDetailView(PermissionRequiredMixin, DetailView):
    queryset = Order.objects.select_related('user').prefetch_related('product')
    permission_required = 'shopapp.view_order'
    context_object_name = 'order'


class ProductCreateView(UserPassesTestMixin,CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')
    form_class = ProductForm


class ProductUpdateView(UserPassesTestMixin,UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount','preview'
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def test_func(self):
        product = self.get_object()

        if self.request.user.is_superuser:
            return True
        elif self.request.user.has_perm('shopapp.change_product') and product.created_by == self.request.user:
            return True
        else:
            return False

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )
        return response


    def get_success_url(self):
        return reverse('shopapp:products_details',
                       kwargs={'pk': self.object.pk})


class ProductDeleteView(DeleteView):
    template_name = 'shopapp/product_confirm_delete.html'
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'delivery_address', 'product', 'user'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse('shopapp:order_details',
                       kwargs={'pk': self.object.pk})


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'shopapp/order_confirm_delete.html'
    success_url = reverse_lazy('shopapp:orders_list')


class OrderCreateView(CreateView):
    model = Order
    fields = 'delivery_address', 'user', 'product', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')


class UserOrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'shopapp/user_orders.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        self.owner = get_object_or_404(User, pk=user_id)
        if not self.request.user == self.owner or not self.request.user.is_staff:
            return HttpResponse({'error': 'У вас нет прав на просмотр заказов!'})
        return Order.objects.filter(user=self.owner).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = self.owner
        context['cache_owner_key'] = f'owner_{self.owner.pk}_pk'
        return context


class UserOrdersExportView(View, LoginRequiredMixin):

    def get(self,request: HttpRequest, user_id):
        owner = get_object_or_404(User, pk=user_id)

        if not request.user == owner or not request.user.is_staff:
            return HttpResponse({'error': 'У вас нет прав на просмотр заказов!'})

        cache_key = f'user_orders_key_{owner.pk}'
        cache_data = cache.get(cache_key)

        if cache_data is not None:
            return JsonResponse(json.loads(cache_data), safe=False)

        orders = Order.objects.filter(user=owner).order_by('pk')

        serializer = OrderSerializer(orders, many=True)
        data = serializer.data

        cache.set(cache_key, json.dumps(data), timeout=60)

        return JsonResponse(data, safe=False)




