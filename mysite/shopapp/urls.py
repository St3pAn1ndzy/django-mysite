from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShopIndexView,
    ProductDetailsView,
    OrdersListView,
    ProductListView,
    ProductUpdateView,
    ProductCreateView,
    ProductDeleteView,
    OrderDetailsView,
    OrderUpdateView,
    OrderDeleteView,
    OrderCreateView,
    OrdersExportView,
    ProductsViewSet,
    OrdersViewSet,
    LatestProductsFeed,
    UserOrdersListView, UserOrdersExportView,
)

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductsViewSet)
routers.register('orders', OrdersViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='shop_index'),
    path('api/', include(routers.urls), name='api'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='products_create'),
    path('products/<int:pk>', ProductDetailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/archive', ProductDeleteView.as_view(), name='product_archive'),
    path('products/latest/feed/', LatestProductsFeed(), name='products_feed'),
    path('orders/', OrdersListView.as_view(), name='orders_list'),
    path('orders/create', OrderCreateView.as_view(), name='orders_create'),
    path('orders/<int:pk>', OrderDetailsView.as_view(), name='orders_details'),
    path('orders/<int:pk>/update', OrderUpdateView.as_view(), name='orders_update'),
    path('orders/<int:pk>/delete', OrderDeleteView.as_view(), name='orders_delete'),
    path('users/<int:user_id>/orders/', UserOrdersListView.as_view(), name='orders_user'),
    path('users/<int:user_id>/orders/export/', UserOrdersExportView.as_view(), name='orders_user_export'),
    path('orders/export/', OrdersExportView.as_view(), name='orders_export'),
]
