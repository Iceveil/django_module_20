from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (
                    ShopAppView,
                    GroupsListView,
                    ProductDetailsView,
                    ProductsListView,
                    OrdersListView,
                    ProductCreateView,
                    OrderDetailView,
                    ProductUpdateView,
                    ProductDeleteView,
                    OrderUpdateView,
                    OrderDeleteView,
                    OrderCreateView,
                    ProductViewSet,
                    OrderViewSet,
                    LatestProductsFeed,
                    UserOrdersListView,
                    UserOrdersExportView,
                    )

routers = DefaultRouter()
routers.register('products',ProductViewSet,)
routers.register('orders', OrderViewSet)

app_name = 'shopapp'
urlpatterns = [
    path('', cache_page(60*2)(ShopAppView.as_view()), name='index'),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archived', ProductDeleteView.as_view(), name='product_delete'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_form'),
    path('orders/create/', OrderCreateView.as_view(), name='create_order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_details'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path('api/', include(routers.urls)),
    path('products/latest/feed/', LatestProductsFeed(), name='products_feed'),
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='user_orders'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='user_orders_export'),

]
